from django.forms import ModelForm

import models

class NamespaceGroupForm(ModelForm):
    class Meta:
        model = models.NamespaceGroup
        fields = ['group']


class NamespaceForm(ModelForm):
    class Meta:
        model = models.Namespace
        fields = ['name', 'type']

##### Prerequisite Forms ######
class PrerequisiteForNamespaceForm(ModelForm):
    class Meta:
        model = models.PrerequisiteForNamespace
        fields = ['logic']
    

class NumericConditionForPrerequisiteForm(ModelForm):
    class Meta:
        model = models.NumericConditionForPrerequisite
        fields = ['type', 'value', 'comparator']
        
        
class LogicalConditionForPrerequisiteForm(ModelForm):
    class Meta:
        model = models.LogicalConditionForPrerequisite
        fields = ['key', 'value', 'bool']
    
##### Numeric Forms #####
class NumericForNamespaceForm(ModelForm):
    class Meta:
        model = models.NumericForNamespace
        fields = ['type', 'value', 'stack_type']
        
        
class ConditionForNumericForm(ModelForm):
    class Meta:
        model = models.ConditionForNumeric
        fields = ['logic']
        
class NumericConditionForNumericForm(ModelForm):
    class Meta:
        model = models.NumericConditionForNumeric
        fields = ['type', 'value']
        
        
class LogicalConditionForNumericForm(ModelForm):
    class Meta:
        model = models.LogicalConditionForNumeric
        fields = ['key', 'value']

class LogicalForNamespaceForm(ModelForm):
    class Meta:
        model = models.LogicalForNamespace
        fields = [ 'key', 'value']

class ConditionForLogicalForm(ModelForm):
    class Meta:
        model = models.ConditionForLogical
        fields = ['logic']

class LogicalConditionForLogicalForm(ModelForm):
    class Meta:
        model = models.LogicalConditionForLogical
        fields = ['key', 'value']
        
        
class NumericConditionForLogicalForm(ModelForm):
    class Meta:
        model = models.NumericConditionForLogical
        fields = ['type', 'value']

class ChoiceForm(ModelForm):
    class Meta:
        model = models.Choice
        fields = ['groups', 'namespace_names', 'namespace']

class SubspaceForNamespaceForm(ModelForm):
    class Meta:
        model = models.SubspaceForNamespace
        fields = []
        
class ConditionForSubspaceForm(ModelForm):
    class Meta:
        model = models.ConditionForSubspace
        fields = ['logic']

class LogicalConditionForSubspaceForm(ModelForm):
    class Meta:
        model = models.LogicalConditionForSubspace
        fields = ['key', 'value']
        
class NumericConditionForSubspaceForm(ModelForm):
    class Meta:
        model = models.NumericConditionForSubspace
        fields = ['type', 'value']
