from django.db import models

# Create your models here.
class NamespaceGroup(models.Model):
    group = models.CharField(max_length=64)
    
    def __unicode__(self):
        return self.group
    

class Condition(models.Model):
    LOGIC = (("AND", "AND"),
             ("OR", "OR"),
             ("NAND", "NAND"),
             ("NOR", "NOR"))
    logic = models.CharField(max_length=3,
                             choices=LOGIC,
                             default='&&')
    

class Numeric(models.Model):
    type = models.CharField(max_length=64)
    value = models.CharField(max_length=64)


class NumericCondition(Numeric):
    COMPARATOR = (("=", "equals"),
                  (">", "greater than"),
                  ("<", "less than"),
                  (">=", "greater than or equal to"))
    comparator = models.CharField(max_length=50,
                                  choices=COMPARATOR,
                                  default=">=")


class Logical(models.Model):
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=64)


class LogicalCondition(Logical):
    BOOL = (("in", "has this property"),
            ("not in", "does not have this property"),)
    bool = models.CharField(max_length=10, choices=BOOL, default="in")

################ Attributes for Namespace ##################
class Namespace(models.Model):
    NAMESPACE_TYPES = (('Abstract', 'Abstract'),
                       ('Action', 'Action'),
                       ('Attack', 'Attack'),
                       ('Effect', 'Effect'))
    name = models.CharField(max_length=64, unique=True)
    groups = models.ManyToManyField(NamespaceGroup, blank=True)
    type = models.CharField(max_length=64, choices=NAMESPACE_TYPES, default="Abstract")
    inherits = models.ManyToManyField("Namespace", blank=True)
    
    def __unicode__(self):
        return self.name

class NumericForNamespace(Numeric):
    STACK_TYPES = (("Base", "Base"),
                   ("Enhancement", "Enhancement"),
                   ("Morale", "Morale"),
                   ("Sacred", "Sacred"),
                   ("Profane", "Profane"),
                   ("Deflection", "Deflection"),
                   ("Dodge", "Dodge"),)
    target = models.ForeignKey(Namespace, related_name="numeric_target")
    stack_type = models.CharField(max_length=64, choices=STACK_TYPES, default="Base")
    namespace = models.ForeignKey(Namespace, related_name="numeric_parent")

class LogicalForNamespace(Logical):
    target = models.ForeignKey(Namespace, related_name="logical_target")
    namespace = models.ForeignKey(Namespace, related_name="logcial_parent")
    

class Choice(models.Model):
    groups = models.ManyToManyField(NamespaceGroup, blank=True)
    namespace_names = models.ManyToManyField(Namespace, related_name='choice_namespace_names', blank=True)
    namespace = models.ForeignKey(Namespace, related_name='choice_namespace_from')


class SubspaceForNamespace(models.Model):
    target = models.ForeignKey(Namespace, related_name="target")
    namespace = models.ForeignKey(Namespace, related_name="belongs_to")


################ Prerequisite for Namespace ##################
class PrerequisiteForNamespace(Condition):
    parent = models.ForeignKey(Namespace)
    
class NumericConditionForPrerequisite(NumericCondition):
    condition = models.ForeignKey(PrerequisiteForNamespace)
    
class LogicalConditionForPrerequisite(LogicalCondition):
    condition = models.ForeignKey(PrerequisiteForNamespace)
    
################ Condition for Numeric #######################
class ConditionForNumeric(Condition):
    parent = models.ForeignKey(NumericForNamespace)

class NumericConditionForNumeric(NumericCondition):
    condition = models.ForeignKey(ConditionForNumeric)

class LogicalConditionForNumeric(LogicalCondition):
    condition = models.ForeignKey(ConditionForNumeric)

################# Condition for Logical ######################
class ConditionForLogical(Condition):
    parent = models.ForeignKey(LogicalForNamespace)

class LogicalConditionForLogical(LogicalCondition):
    condition = models.ForeignKey(ConditionForLogical)

class NumericConditionForLogical(NumericCondition):
    condition = models.ForeignKey(ConditionForLogical)

################# Condition for Subspace #####################
class ConditionForSubspace(Condition):
    parent = models.ForeignKey(SubspaceForNamespace)
    
class LogicalConditionForSubspace(LogicalCondition):
    condition = models.ForeignKey(ConditionForSubspace)
    
class NumericConditionForSubspace(NumericCondition):
    condition = models.ForeignKey(ConditionForSubspace)
