// TODO: Once your application is deployed, copy an API id here so that the frontend could interact with it
// export const apiEndpoint = "http://localhost:8080";
export const apiEndpoint = "https://s1kjjye3gi.execute-api.us-east-1.amazonaws.com/api";

export const authConfig = {
  // TODO: Create an Auth0 application and copy values from it into this map
  domain: 'kungfulucky7.us.auth0.com',            // Auth0 domain
  clientId: 'sSGU8JrhHWRG6poOIDEDjcCiy4XXY0q6',          // Auth0 client id
  // callbackUrl: 'http://localhost:3000/callback',
  callbackUrl: 'http://file-upload-frontend-dev.us-east-1.elasticbeanstalk.com/callback'
}
