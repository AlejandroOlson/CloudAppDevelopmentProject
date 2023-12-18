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
	const authenticator = new IamAuthenticator({ apikey: "1Wq08to7Fxiz5LZplhhZOvvRqpR8KRc3vuXNJbu3PjDw" });
    const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl("https://1d8ebd47-6176-403f-95b8-3c90d5aa2921-bluemix.cloudantnosqldb.appdomain.cloud");
      try {
          let result = await cloudant.postAllDocs({
              db: 'dealerships',
              startKey: '8cc*',
              includeDocs: true,
          });
          return result;
      } catch (error) {
          return { error: error.description };
      }
}