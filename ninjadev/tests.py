import time

from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from ninjadev.models import Namespace
from ninjadev.models import NamespaceGroup

from ninjadev.models import PrerequisiteForNamespace
from ninjadev.models import NumericConditionForPrerequisite
from ninjadev.models import LogicalConditionForPrerequisite

from ninjadev.models import NumericForNamespace
from ninjadev.models import LogicalForNamespace
from ninjadev.models import SubspaceForNamespace

from ninjadev.models import Choice

# Create your tests here.

class NamespaceObjectTests(TestCase):
    
    def test_name(self):
        ns = Namespace.objects.create(name="Test Namespace")
        self.assertEquals(str(ns), "Test Namespace")
        
class NamespaceIntegrationTests(LiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(NamespaceIntegrationTests, cls).setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(NamespaceIntegrationTests, cls).tearDownClass()
        
    def test_create_namespace(self):
        
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/'))
        input_search = self.selenium.find_element_by_id("search_namespaces")
        input_search.send_keys("Test Namespace")
        self.selenium.execute_script("document.getElementById(\"navigate\").value = \"create\";")
        input_search.send_keys(Keys.ENTER)
        
        # Make sure it is listed
        self.assertEqual(
            self.selenium.find_element_by_name('name').get_attribute("value"),
            'Test Namespace' )
        
    def test_add_namespace_group(self):
        ns = "Namespace Groups Test"
        ns_slug = "Namespace-Groups-Test"
        grp = "Namespace Test Group"
        Namespace.objects.create(name=ns)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s/' % ns_slug))
        add_groups = self.selenium.find_element_by_id("typeahead_groups")
        add_groups.send_keys(grp)
        add_groups.send_keys(Keys.ENTER)
        result = NamespaceGroup.objects.filter(group=grp)
        self.assertTrue(len(result) == 1)
        
    def test_add_inherits(self):
        ns = "Namespace Inherits Test"
        ns_slug = "Namespace-Inherits-Test"
        inherit = "Namespace To Inherit"
        Namespace.objects.create(name=inherit)
        ns_model = Namespace.objects.create(name=ns)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s/' % ns_slug))
        add_inherits = self.selenium.find_element_by_id('typeahead_inherits')
        add_inherits.send_keys(inherit)
        add_inherits.send_keys(Keys.ENTER)
        time.sleep(0.1)
        self.assertTrue(len(ns_model.inherits.all()) == 1)
        
    def test_add_prerequisite(self):
        ns = "Add Prerequisite Test"
        ns_slug = "Add-Prerequisite-Test"
        ns_model = Namespace.objects.create(name=ns)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s/' % ns_slug))
        add_prereq = self.selenium.find_element_by_id('add_prerequisite_button')
        add_prereq.click()
        time.sleep(0.5) # wait for modal to open
        add_condition = self.selenium.find_element_by_id('add_condition')
        add_condition.click()
        time.sleep(0.1) # wait for POST to complete
        prereqs = PrerequisiteForNamespace.objects.filter(parent=ns_model)
        self.assertTrue(len(prereqs) == 1)
        
    def test_add_numeric_condition_to_prerequisite(self):
        ns = "Add Numeric To Prerequisite Test"
        ns_slug = "Add-Numeric-To-Prerequisite-Test"
        ns_model = Namespace.objects.create(name=ns)
        prereq_cond = PrerequisiteForNamespace.objects.create(parent=ns_model)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s/' % ns_slug))
        prereq_table = self.selenium.find_element_by_id('prerequisites')
        add_numeric = prereq_table.find_element_by_name('create_numeric')
        add_numeric.click()
        time.sleep(0.5) # wait for modal to open
        numeric_cond_modal = self.selenium.find_element_by_id("numeric_condition_modal")
        numeric_type = numeric_cond_modal.find_element_by_id("id_type")
        numeric_type.send_keys("Strength")
        numeric_value = numeric_cond_modal.find_element_by_id("id_value")
        numeric_value.send_keys("12")
        add_numeric_done = numeric_cond_modal.find_element_by_name("add_numeric_condition")
        add_numeric_done.click()
        time.sleep(0.1) # wait for POST to complete
        numeric_conditions = NumericConditionForPrerequisite.objects.filter(condition=prereq_cond)
        self.assertTrue(len(numeric_conditions) == 1)
        
    def test_add_logical_condition_to_prerequisite(self):
        ns = "Add Logical To Prerequisite Test"
        ns_slug = "Add-Logical-To-Prerequisite-Test"
        ns_model = Namespace.objects.create(name=ns)
        prereq_cond = PrerequisiteForNamespace.objects.create(parent=ns_model)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s/' % ns_slug))
        prereq_table = self.selenium.find_element_by_id('prerequisites')
        add_logical = prereq_table.find_element_by_name("create_logical")
        add_logical.click()
        time.sleep(0.5)        
        logical_cond_modal = self.selenium.find_element_by_id("logical_condition_modal")
        logical_key = logical_cond_modal.find_element_by_id("id_key")
        logical_key.send_keys("Equipment")
        logical_value = logical_cond_modal.find_element_by_id("id_value")
        logical_value.send_keys("Medium Armor")
        add_logical_done = logical_cond_modal.find_element_by_name("add_logical_condition")
        add_logical_done.click()
        time.sleep(0.1) # wait for POST to complete
        logical_conditions = LogicalConditionForPrerequisite.objects.filter(condition=prereq_cond)
        self.assertTrue(len(logical_conditions) == 1)
        
    def test_add_numeric(self):
        ns = "Add Numeric Test"
        ns_slug = "Add-Numeric-Test"
        ns_model = Namespace.objects.create(name=ns)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s' % ns_slug))
        add_numeric = self.selenium.find_element_by_id("button_create_numeric")
        add_numeric.click()
        time.sleep(0.5)
        numeric_modal = self.selenium.find_element_by_id("numeric_modal")
        textbox_type = numeric_modal.find_element_by_name("type")
        textbox_type.send_keys("Strength")
        textbox_value = numeric_modal.find_element_by_name('value')
        textbox_value.send_keys('2')
        textbox_stack = numeric_modal.find_element_by_name('stack_type')
        textbox_stack.send_keys('Base')
        button_add_numeric = numeric_modal.find_element_by_name('add_numeric')
        button_add_numeric.click()
        time.sleep(0.1)
        numerics = NumericForNamespace.objects.filter(target=ns_model)
        self.assertTrue(len(numerics) == 1)
        
    def test_add_logical(self):
        ns = "Add Logical Test"
        ns_slug = "Add-Logical-Test"
        ns_model = Namespace.objects.create(name=ns)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s' % ns_slug))
        add_logical = self.selenium.find_element_by_id("button_create_logical")
        add_logical.click()
        time.sleep(0.5)
        logical_modal = self.selenium.find_element_by_id('logical_modal')
        textbox_key = logical_modal.find_element_by_name("key")
        textbox_key.send_keys("Equipment")
        textbox_value = logical_modal.find_element_by_name('value')
        textbox_value.send_keys("Light Armor")
        textbox_value.send_keys(Keys.ENTER)
        time.sleep(0.1)
        logicals = LogicalForNamespace.objects.filter(target=ns_model)
        self.assertTrue(len(logicals) == 1)
        
    def test_add_subspace(self):
        ns = "Add Subspace Test"
        ns_slug = "Add-Subspace-Test"
        ns_model = Namespace.objects.create(name=ns)
        ns_target = "Target Subspace"
        ns_target_model = Namespace.objects.create(name=ns_target)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s' % ns_slug))
        add_subspace = self.selenium.find_element_by_id('button_create_subspace')
        add_subspace.click()
        time.sleep(0.5)
        subspace_modal = self.selenium.find_element_by_id('subspace_modal')
        textbox_target = subspace_modal.find_element_by_name('target_namespace')
        textbox_target.send_keys(ns_target)
        button_modal_add_subspace = self.selenium.find_element_by_id('add_subspace')
        button_modal_add_subspace.click()
        time.sleep(0.1) # due to typeahead
        subspaces = SubspaceForNamespace.objects.filter(target=ns_target_model)
        self.assertTrue(len(subspaces) == 1)
        
    def test_add_choice(self):
        ns = "Add Namespace Subspace Choice"
        ns_slug = "Add-Namespace-Subspace-Choice"
        ns_model = Namespace.objects.create(name=ns)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s' % ns_slug))
        add_choice = self.selenium.find_element_by_name('add_choice_to_namespace')
        add_choice.click()
        time.sleep(0.1)
        choices = Choice.objects.filter(namespace=ns_model)
        self.assertTrue(len(choices) == 1)
        
    def test_add_choice_nsgroup(self):
        ns = "Add Namespace Group Choice"
        ns_slug = "Add-Namespace-Group-Choice"
        ns_model = Namespace.objects.create(name=ns)
        selection = Choice.objects.create(namespace=ns_model)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s' % ns_slug))
        div_choice = self.selenium.find_element_by_id('choices')
        textbox_add_nsgroup = div_choice.find_element_by_id('group1')
        textbox_add_nsgroup.send_keys("Class Level")
        textbox_add_nsgroup.send_keys(Keys.ENTER)
        time.sleep(0.1)
        self.assertTrue(len(selection.groups.all()) == 1)
        
    def test_add_choice_namespace(self):
        ns = "Add Namespace Specific Choice"
        ns_slug = "Add-Namespace-Specific-Choice"
        ns_model = Namespace.objects.create(name=ns)
        selection = Choice.objects.create(namespace=ns_model)
        self.selenium.get("%s%s" % (self.live_server_url, '/ninjadev/%s' % ns_slug))
        div_choice = self.selenium.find_element_by_id('choices')
        textbox_add_specific_ns = div_choice.find_element_by_id('namespace1')
        textbox_add_specific_ns.send_keys("Fake Choice")
        textbox_add_specific_ns.send_keys(Keys.ENTER)
        time.sleep(0.1)
        self.assertTrue(len(selection.namespace_names.all()) == 1)
        created = Namespace.objects.filter(name="Fake Choice")
        self.assertTrue(len(created) == 1)
    