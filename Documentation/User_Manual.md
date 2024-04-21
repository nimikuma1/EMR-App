o	Provide information on deployment of the application.

We have deployed the application on AWS. We created EC2 Instance and launched an EC2 (Elastic Compute Cloud) instance to host our application. We cloned our application code to the EC2 instance using a Git repository. We installed required dependencies (e.g., Python packages) on the EC2 instance.

o	Provide basic user instructions in order to utilize the application fully and show off all features.

Navigate to this URL: http://18.188.93.0:5000/

Type in "priorauth" for Username 

Type in "DivyaNimisha123" for Password 

![image](https://github.com/nimikuma1/EMR-App/assets/166041511/d740bd6d-5a85-4084-b059-eee613833206)

Click "Login"
You should see:

![image](https://github.com/nimikuma1/EMR-App/assets/166041511/284e1395-7d95-4701-a96f-235956b21149)

We can select a patient from the drop down and click "Prior Auth" button.
The ICD code and Procedural code gets updated automatically from ChatGPT as shown below. Once the ICD code and procedure codes are updated in the EMR database, a FHIR API is invoked to submit the prior auth data to the Payor system. The payor application sends the response as "Submitted". 
The Prior Auth Status gets updated as "Submitted" as shown below.

![image](https://github.com/nimikuma1/EMR-App/assets/166041511/66079a16-800e-4db2-a69d-e7bc627c12cd)

The corresponding member details are pushed to the Payor System Application automatically as shown below.

![image](https://github.com/nimikuma1/EMR-App/assets/166041511/0fc2ea18-3262-49d8-8e3f-a04e44735b5e)
