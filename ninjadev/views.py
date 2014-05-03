from django.core.urlresolvers import reverse

from ninjadev.models import Namespace
from ninjadev.models import NamespaceGroup
from ninjadev.models import Choice

from ninjadev.models import PrerequisiteForNamespace
from ninjadev.models import NumericConditionForPrerequisite
from ninjadev.models import LogicalConditionForPrerequisite

from ninjadev.models import NumericForNamespace
from ninjadev.models import ConditionForNumeric
from ninjadev.models import NumericConditionForNumeric
from ninjadev.models import LogicalConditionForNumeric

from ninjadev.models import LogicalForNamespace
from ninjadev.models import ConditionForLogical
from ninjadev.models import NumericConditionForLogical
from ninjadev.models import LogicalConditionForLogical

from ninjadev.models import SubspaceForNamespace
from ninjadev.models import ConditionForSubspace
from ninjadev.models import NumericConditionForSubspace
from ninjadev.models import LogicalConditionForSubspace

import ninjadev.forms
import ninjadin.settings

from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

def login_required(view):
    def f(request, *args, **kwargs):
        if request.user.is_anonymous():
            return view(request, *args, **kwargs)
        return HttpResponseRedirect(ninjadin.settings.LOGIN_REDIRECT_URL)

class NamespaceLists():
    names = Namespace.objects.all()
    groups = NamespaceGroup.objects.all()

class NamespaceData():
    def __init__(self, name):
        self.name = name.replace('-', ' ')
        self.slug_name = name.replace(' ', '-')
        self.model = Namespace.objects.get(name=self.name)
        self.groups = self.model.groups.all()
        self.inherits = self.model.inherits.all()
        self.forms = {}
        self.forms["Namespace"] = ninjadev.forms.NamespaceForm(instance=self.model)
        
        self.forms["PrerequisiteForNamespaceForm"] = ninjadev.forms.PrerequisiteForNamespaceForm()
        self.forms["NumericConditionForPrerequisiteForm"] = ninjadev.forms.NumericConditionForPrerequisiteForm()
        self.forms["LogicalConditionForPrerequisiteForm"] = ninjadev.forms.LogicalConditionForPrerequisiteForm()
        
        self.forms["NumericForNamespaceForm"] = ninjadev.forms.NumericForNamespaceForm()
        self.forms["ConditionForNumericForm"] = ninjadev.forms.ConditionForNumericForm()
        self.forms["LogicalConditionForNumericForm"] = ninjadev.forms.LogicalConditionForNumericForm()
        self.forms["NumericConditionForNumericForm"] = ninjadev.forms.NumericConditionForNumericForm()
        
        self.forms["LogicalForNamespaceForm"] = ninjadev.forms.LogicalForNamespaceForm()
        self.forms["ConditionForLogicalForm"] = ninjadev.forms.ConditionForLogicalForm()
        self.forms["NumericConditionForLogicalForm"] = ninjadev.forms.NumericConditionForLogicalForm()
        self.forms["LogicalConditionForLogicalForm"] = ninjadev.forms.LogicalConditionForLogicalForm()
        
        self.forms["SubspaceForNamespaceForm"] = ninjadev.forms.SubspaceForNamespaceForm()
        
        self.prerequisites = [Conditions(i, NumericConditionForPrerequisite, LogicalConditionForPrerequisite) for i in PrerequisiteForNamespace.objects.filter(parent=self.model.id)]

        self.numeric_columns = ["Namespace", "Statistic", "Type", "Value", "Logic", "Expression", ""] 
        self.numerics = [NumericData(i) for i in NumericForNamespace.objects.filter(namespace=self.model.id)]

        self.logical_columns = ['Namespace', "Apply/Remove/Negate", "Key", "Value", "Logic", "Expression", ""]
        self.logicals = [LogicalData(i) for i in LogicalForNamespace.objects.filter(namespace=self.model.id)]

        self.subspaces = [SubspaceData(i) for i in SubspaceForNamespace.objects.filter(namespace=self.model.id)]
        self.subspace_columns = ['Namespace', 'Logic', 'Expression', ""]

        self.choices = [ChoiceData(i) for i in Choice.objects.filter(namespace=self.model.id)]

class ConditionalData(object):
    def __init__(self, model):
        self.model = model
        self.conditions = [Conditions(i, self.NUMERIC_CLS, self.LOGICAL_CLS) for i in self.CONDITION_CLS.objects.filter(parent=self.model)]
        self.total_conditions_plusone = sum([i.total_conditions_plusone for i in self.conditions]) + 1

class NumericData(ConditionalData):
    NUMERIC_CLS = NumericConditionForNumeric
    LOGICAL_CLS = LogicalConditionForNumeric
    CONDITION_CLS = ConditionForNumeric
    def __init__(self, model):
        super(NumericData, self).__init__(model)
        self.fields = [model.namespace, model.type, model.stack_type, model.value]
        
class LogicalData(ConditionalData):
    NUMERIC_CLS = NumericConditionForLogical
    LOGICAL_CLS = LogicalConditionForLogical
    CONDITION_CLS = ConditionForLogical
    def __init__(self, model):
        super(LogicalData, self).__init__(model)
        self.fields = [model.namespace, "", model.key, model.value]

class SubspaceData(ConditionalData):
    NUMERIC_CLS = NumericConditionForSubspace
    LOGICAL_CLS = LogicalConditionForSubspace
    CONDITION_CLS = ConditionForSubspace
    def __init__(self, model):
        super(SubspaceData, self).__init__(model)
        self.fields = [model.target]

class Conditions():
    def __init__(self, model, numeric_cls, logical_cls):
        self.model = model
        self.numeric_conditions = numeric_cls.objects.filter(condition=self.model)
        self.logical_conditions = logical_cls.objects.filter(condition=self.model)
        self.total_conditions_plusone = len(self.numeric_conditions) + len(self.logical_conditions) + 1
        
class ChoiceData():
    def __init__(self, model):
        self.model = model
        self.namespace_names = model.namespace_names.all()
        self.groups = model.groups.all()
        

class NamespaceName():
    """  Helper class for creating a string/slug pair """
    def __init__(self, name):
        self.name = name.replace('-', ' ')
        self.slug = name.replace(' ', '-')

class NamespaceView(object):
    def __init__(self, slug_name):
        pass
    
    @classmethod
    def search_read(cls, request):
        namespaces = [NamespaceName(str(i)) for i in Namespace.objects.all()]
        search_result = namespaces
        if request.method == 'POST':
            model = Namespace.objects.filter(name=request.POST["search_namespaces"])
            if model:
                return HttpResponseRedirect(reverse("namespaces-base") + "%s/" % NamespaceName(request.POST["search_namespaces"]).slug)
            if request.POST["operation"] == "search":
                search_result = [NamespaceName(str(i)) for i in Namespace.objects.filter(name__contains=request.POST["search_namespaces"])]
            elif request.POST["operation"] == "create":
                if not request.user.is_authenticated():
                    return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
                model = Namespace.objects.create(name=request.POST["search_namespaces"])
                redirect = reverse("namespaces-base") + "%s/" % request.POST["search_namespaces"].replace(' ', '-')
                return HttpResponseRedirect(redirect)
        context = RequestContext(request, {'namespaces': NamespaceLists(),
                                           'search_result': search_result})
        t = get_template("namespace_search.html")
        html = t.render(context)
        return HttpResponse(html)
    
    @classmethod
    def update_delete(cls, request, slug_name):
        namespace = NamespaceData(slug_name)
        redirect = reverse("namespaces-base") + "%s/" % slug_name
        if request.method == 'POST':
            if not request.user.is_authenticated():
                return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
            if "namespace_delete" in request.POST:
                namespace.model.delete()
                return HttpResponseRedirect(redirect)
            elif "remove_item" in request.POST:
                namespace_group = NamespaceGroup.objects.get(group=request.POST["remove_item"])
                namespace.model.groups.remove(namespace_group)
                return HttpResponseRedirect(redirect)
            elif "save" in request.POST:
                namespace.model.name = request.POST["name"]
                namespace.model.type = request.POST["type"]
                namespace.model.save()
                redirect = reverse("namespaces-base") + "%s/" % namespace.model.name.replace(' ', '-')
                return HttpResponseRedirect(redirect)
            elif "new_list_item" in request.POST:
                if request.POST["choice_type"] == "groups":
                    try:
                        existing = NamespaceGroup.objects.get(group=request.POST["new_list_item"])
                        namespace.model.groups.add(existing)
                    except NamespaceGroup.DoesNotExist:
                        if len(request.POST["new_list_item"]) > 0:
                            namespace_group = NamespaceGroup(group=request.POST["new_list_item"])
                            namespace_group.save()
                            namespace.model.groups.add(namespace_group)
                elif request.POST["choice_type"] == "inherits":
                    try:
                        existing = Namespace.objects.get(name=request.POST["new_list_item"])
                        namespace.model.inherits.add(existing)
                    except Namespace.DoesNotExist:
                        pass
                return HttpResponseRedirect(redirect)
        context = RequestContext(request, {
                            'namespace': namespace,
                            'namespaces': NamespaceLists()})
        t = get_template("namespace_edit.html")
        html = t.render(context)
        return HttpResponse(html)

class NumericTableDefinition(object):
    name = "numeric"
    TableModel = NumericForNamespace
    TableModelForm = ninjadev.forms.NumericForNamespaceForm
    ConditionModel = ConditionForNumeric
    ConditionModelForm = ninjadev.forms.ConditionForNumericForm
    NumericModel = NumericConditionForNumeric
    NumericModelForm = ninjadev.forms.NumericConditionForNumericForm
    LogicalModel = LogicalConditionForNumeric
    LogicalModelForm = ninjadev.forms.LogicalConditionForNumericForm
    
class PrerequisiteTableDefinition(object):
    name = "prerequisite"
    TableModel = Namespace
    ConditionModel = PrerequisiteForNamespace
    ConditionModelForm = ninjadev.forms.PrerequisiteForNamespaceForm
    NumericModel = NumericConditionForPrerequisite
    NumericModelForm = ninjadev.forms.NumericConditionForPrerequisiteForm
    LogicalModel = LogicalConditionForPrerequisite
    LogicalModelForm = ninjadev.forms.LogicalConditionForPrerequisiteForm

class LogicalTableDefinition(object):
    name = "logical"
    TableModel = LogicalForNamespace
    TableModelForm = ninjadev.forms.LogicalForNamespaceForm
    ConditionModel = ConditionForLogical
    ConditionModelForm = ninjadev.forms.ConditionForLogicalForm
    NumericModel = NumericConditionForLogical
    NumericModelForm = ninjadev.forms.NumericConditionForLogicalForm
    LogicalModel = LogicalConditionForLogical
    LogicalModelForm = ninjadev.forms.LogicalConditionForLogicalForm
    
class SubspaceTableDefinition(object):
    name = "subspace"
    TableModel = SubspaceForNamespace
    TableModelForm = ninjadev.forms.SubspaceForNamespaceForm
    ConditionModel = ConditionForSubspace
    ConditionModelForm = ninjadev.forms.ConditionForSubspaceForm
    NumericModel = NumericConditionForSubspace
    NumericModelForm = ninjadev.forms.NumericConditionForSubspaceForm
    LogicalModel = LogicalConditionForSubspace
    LogicalModelForm = ninjadev.forms.LogicalConditionForSubspaceForm
    
table_dictionary = {"numeric": NumericTableDefinition,
                    "prerequisite": PrerequisiteTableDefinition,
                    "logical": LogicalTableDefinition,
                    "subspace": SubspaceTableDefinition  }

def table_POST_handler(request, slug_name, table_name):
    table = table_dictionary[table_name]
    if request.method == "POST":
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        if "add_%s" % table_name in request.POST:
            namespace = Namespace.objects.get(name=slug_name.replace('-', ' '))
            target = Namespace.objects.get(name=request.POST["target_namespace"])
            inst = table.TableModel(namespace=namespace, target=target)
            new_object = table.TableModelForm(request.POST, instance=inst)
            if new_object.is_valid():
                new_object.save()
        elif "add_condition" in request.POST:
            parent = table.TableModel.objects.get(id=request.POST['condition_modal_hidden_id'])
            inst = table.ConditionModel(parent=parent)
            condition = table.ConditionModelForm(request.POST, instance=inst)
            if condition.is_valid():
                condition.save()
        elif "add_numeric_condition" in request.POST:
            condition = table.ConditionModel.objects.get(id=request.POST['numeric_condition_modal_hidden_id'])
            inst = table.NumericModel(condition=condition)
            numeric = table.NumericModelForm(request.POST, instance=inst)
            if numeric.is_valid():
                numeric.save()
        elif "add_logical_condition" in request.POST:
            condition = table.ConditionModel.objects.get(id=request.POST['logical_condition_modal_hidden_id'])
            inst = table.LogicalModel(condition=condition)
            logical = table.LogicalModelForm(request.POST, instance=inst)
            if logical.is_valid():
                logical.save()
        elif "delete_numeric" in request.POST:
            model = table.NumericModel.objects.get(id=request.POST['numeric_id'])
            model.delete()
        elif "delete_logical" in request.POST:
            model = table.LogicalModel.objects.get(id=request.POST['logical_id'])
            model.delete()
        elif "remove_condition" in request.POST:
            model = table.ConditionModel.objects.get(id=request.POST['condition_id'])
            model.delete()
        elif "remove_from_namespace" in request.POST:
            model = table.TableModel.objects.get(id=request.POST['%s_id' % table.name])
            model.delete()
        redirect = reverse("namespaces-base") + "%s/#%ss" % (slug_name, table_name)
        return HttpResponseRedirect(redirect)

def choice_POST_handler(request, slug_name):
    if request.method == "POST":
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('django.contrib.auth.views.login'))
        if "add_choice_to_namespace" in request.POST:
            namespace = Namespace.objects.get(name=slug_name.replace('-', ' '))
            inst = Choice(namespace=namespace)
            inst.save()
        elif "remove_choice" in request.POST:
            model = Choice.objects.get(id=request.POST["remove_choice"])
            model.delete()
        elif "add_create" in request.POST:
            model = Choice.objects.get(id=request.POST["choice_id"])
            if request.POST["choice_type"] == "group" and len(request.POST["new_list_item"]) > 0:
                namespace_group, created = NamespaceGroup.objects.get_or_create(group=request.POST['new_list_item'])
                namespace_group.save()
                model.groups.add(namespace_group)
            elif request.POST["choice_type"] == "namespace" and len(request.POST["new_list_item"]) > 0:
                new_namespace, created = Namespace.objects.get_or_create(name=request.POST['new_list_item'])
                new_namespace.save()
                model.namespace_names.add(new_namespace)
        elif "remove_item" in request.POST:
            model = Choice.objects.get(id=request.POST["choice_id"])
            if request.POST["choice_type"] == "group":
                namespace_group = NamespaceGroup.objects.get(group=request.POST["remove_item"])
                model.groups.remove(namespace_group)
            elif request.POST["choice_type"] == "namespace":
                ref_namespace = Namespace.objects.get(name=request.POST["remove_item"])
                model.namespace_names.remove(ref_namespace) 
    redirect = reverse("namespaces-base") + "%s/#choices" % slug_name
    return HttpResponseRedirect(redirect)
        