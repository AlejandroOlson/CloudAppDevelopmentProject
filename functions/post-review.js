/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(param) {
	const authenticator = new IamAuthenticator({ apikey: "" }); //API Key
    const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
    });
      
    cloudant.setServiceUrl(""); //service url
    
    const data = CloudantV1.Document = param;
    
    await cloudant.postDocument({
        db: 'reviews',
        document: data
    }).then(response => {
        console.log(response.result);
    });
}
