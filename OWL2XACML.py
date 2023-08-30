# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import xml.etree.ElementTree as ET
import uuid

def get_rule_string():
    return '''
  <Rule RuleId="rule-{}" Effect="Permit">
    <Description>
      {}
    </Description>
    <Target>
      <AnyOf>
        <AllOf>
          <Match MatchId="urn:oasis:names:tc:xacml:1.0:function:string-equal">
            <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">{}</AttributeValue>
            <AttributeDesignator AttributeId="urn:oasis:names:tc:xacml:1.0:subject:subject-id" DataType="http://www.w3.org/2001/XMLSchema#string" MustBePresent="false" Category="urn:oasis:names:tc:xacml:1.0:subject-category:access-subject" />
          </Match>
          <Match MatchId="urn:oasis:names:tc:xacml:1.0:function :string-equal">
            <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">{}</AttributeValue>
            <AttributeDesignator AttributeId="urn:oasis:names:tc:xacml:1.0:action:action-id" DataType="http://www.w3.org/2001/XMLSchema#string" MustBePresent="false" Category="urn:oasis:names:tc:xacml:3.0:attribute-category:action" />
          </Match>
          <Match MatchId="urn:oasis:names:tc:xacml:1.0:function:string-equal">
            <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">{}</AttributeValue>
            <AttributeDesignator AttributeId="urn:oasis:names:tc:xacml:1.0:resource:resource-id" DataType="http://www.w3.org/2001/XMLSchema#string" MustBePresent="false" Category="urn:oasis:names:tc:xacml:3.0:attribute-category:resource" />
          </Match>
        </AllOf>
      </AnyOf>
    </Target>
  </Rule>'''

def add_rule(subject, action, resource, description="Add rule description here"):
    rule_id = str(uuid.uuid1())
    rule_string = get_rule_string().format(rule_id, description, subject, action, resource)
    rule = ET.fromstring(rule_string)
    print(ET.tostring(rule, encoding='utf8').decode('utf8'))
    return rule

def get_xacml_root_template():
    template_string = '''<?xml version="1.0" encoding="utf-8"?>
<Policy xsi:schemaLocation="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17 http://docs.oasis-open.org/xacml/3.0/xacml-core-v3-schema-wd-17.xsd" PolicyId="urn:oasis:names:tc:xacml:2.0:conformance-test:IIIA001:policy" RuleCombiningAlgId="urn:oasis:names:tc:xacml:1.0:rule-combining-algorithm:permit-overrides" Version="1.0" xmlns="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Description>
    Test 1
  </Description>
  <Target />
</Policy>'''
    return ET.fromstring(template_string)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Load the XML content from a file
    xml_file_path = "/Users/rukman/SETU/research/Ontology/university_owl_xml2.owl"  # Replace with the actual file path
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find all <ObjectPropertyAssertion> tags
    object_property_assertions = root.findall('.//{http://www.w3.org/2002/07/owl#}ObjectPropertyAssertion')

    # The data structure which stores all the access between a subject and an object
    access_dict = {}

    # Iterate through each <ObjectPropertyAssertion> tag
    for assertion in object_property_assertions:
        subject = assertion.find('{http://www.w3.org/2002/07/owl#}NamedIndividual').get('IRI')
        object_property = assertion.find('{http://www.w3.org/2002/07/owl#}ObjectProperty').get('IRI')
        object_individual = assertion.find('{http://www.w3.org/2002/07/owl#}NamedIndividual[2]').get('IRI')

        print(f"Subject: {subject}, Object Property: {object_property}, Object Individual: {object_individual}")

        subject = subject.strip('#')
        object_individual = object_individual.strip('#')

        access_dict[subject + '-' + object_individual] = object_property.strip('#').split('_')[1:] # {rukman-data_mining: [read, write]}

    print('-----printing access dict------')

    print(access_dict)

    root = get_xacml_root_template()

    for key, value in access_dict.items():
        subject_resource_split = key.split('-')
        subject = subject_resource_split[0]
        resource = subject_resource_split[1]

        for action in value:
            root.append(add_rule(subject, action, resource))

    #if none of the above rules are permitted, then deny
    root.append(ET.fromstring('<Rule RuleId="Deny everything else" Effect="Deny"></Rule>'))

    print('------ print whole policy ----------')
    print(ET.tostring(root, encoding='utf-8').decode('utf-8'))

    #uncomment the below code the save the generated XACML policy in a file path

    # print('--------saving policy---------')
    # # Save the root element to an XML file
    # output_xml_file = "output_policy.xml"  # Replace with the desired output file path
    # tree = ET.ElementTree(root)
    # tree.write(output_xml_file, encoding="utf-8", xml_declaration=True)