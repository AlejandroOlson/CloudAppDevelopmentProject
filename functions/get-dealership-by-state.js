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
	const authenticator = new IamAuthenticator({ apikey: "" });
    const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl("");
      try {
          let dealerships = await cloudant.postAllDocs({
              db: 'dealerships',
              startKey: '8cc*',
              includeDocs: true,
          });
          
          
          for (dealers in dealerships) {
              if (dealers["state"] == "TX") {
                  return {"message": "FOUND!"};
              }
          }
          
      } catch (error) {
          return { error: error.description };
      }
}