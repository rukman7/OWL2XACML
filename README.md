# OWL2XACML
Research work prototype for converting basic ABAC policies represented in OWL to XACML

## Requirements
1. LUAS PDP - Luas is a nodejs based PDP which accepts XACML request and generates XACML response

Setup and installation steps for Luas: https://npm.io/package/luas

2. Node - version 18 (A dependency of python)
3. Python 3 (For running OWL to XACML script)
4. Protege - For creating and updating ontology

## Getting started

1. Setup Luas npm using the link provided in the requirements section.
2. Clone the repo using the command : `git clone https://github.com/rukman7/OWL2XACML.git`
3. Replace file path at line 53 in OWL2XACML.py with the OWL ontology file. You can create your own ontology(Steps given in the next section) or use the sample ontology file provided (University_owl_xml2.owl)
4. Run OWL2XACML to generate XACML policy for the provided ontology file. 
5. Use the generated policy file as an input to Luas PDP.

sample code for using Luas:

```javascript
const Luas = require('../xacml/luas');
(async () => {
const luas = await Luas.prototype.getPDPInstance(['./IIIA001Policy.xacml3.xml']);
const decision = await luas.evaluate('./IIIA001Request.xacml3.xml');
console.log(decision)   
})();

```

6. From the above sample code `const decision = await luas.evaluate('./IIIA001Request.xacml3.xml');` is used to evaluate a XACML request.
7. Output can be observed in the console. 

## Data model

Refer the below image for the data model that is currently supported. If you are creating your own ontology make sure the ontology is created based on this data model.

## Screenshots

#### Sample request
```xml
<?xml version="1.0" encoding="utf-8"?>
<Request xsi:schemaLocation="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17 http://docs.oasis-open.org/xacml/3.0/xacml-core-v3-schema-wd-17.xsd" ReturnPolicyIdList="false" CombinedDecision="false" xmlns="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Attributes Category="urn:oasis:names:tc:xacml:1.0:subject-category:access-subject">
    <Attribute IncludeInResult="true" AttributeId="urn:oasis:names:tc:xacml:1.0:subject:subject-id">
      <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">Rukmangathan</AttributeValue>
    </Attribute>
  </Attributes>
  <Attributes Category="urn:oasis:names:tc:xacml:3.0:attribute-category:resource">
    <Attribute IncludeInResult="true" AttributeId="urn:oasis:names:tc:xacml:1.0:resource:resource-id">
      <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">Data_mining</AttributeValue>
    </Attribute>
  </Attributes>
  <Attributes Category="urn:oasis:names:tc:xacml:3.0:attribute-category:action">
    <Attribute IncludeInResult="true" AttributeId="urn:oasis:names:tc:xacml:1.0:action:action-id">
      <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#string">read</AttributeValue>
    </Attribute>
  </Attributes>
</Request>
```

#### Sample response - Permit

#### Sample response - Deny

#### Sample python output of the python script