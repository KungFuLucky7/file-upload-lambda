# file-upload-lambda
File Upload Lambda - Written in AWS Chalice & Node.js

This is the final Capstone project for Udagram.
The project is a File Upload app that's a hybrid of Serverless and Microservices technologies on AWS.

The backend is empowered by AWS Chalice [Python Serverless Microframework for AWS](https://github.com/aws/chalice)
while the frontend is built with Node.js, React JavaScript library deployed with AWS Elastic Beanstalk.

The backend consists of Python Lambda functions while the frontend applies a docker-compose.yml
that containerizes an NGINX reverse proxy and a Node.js container for the web app.

The File Upload app repository URL:
https://github.com/KungFuLucky7/file-upload-lambda
The repo has used both AWS CodeBuild & CodePipeline and Travis CI for CI/CD (Continuous Integration/Continuous Deployment).

Backend File Upload API URL:
https://s1kjjye3gi.execute-api.us-east-1.amazonaws.com/api/
e.g. 
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2t1bmdmdWx1Y2t5Ny51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA0NDU3MTAyOTM2NzI0NjM0NzAiLCJhdWQiOiJzU0dVOEpyaEhXUkc2cG9PSURFRGpjQ2l5NFhYWTBxNiIsImlhdCI6MTYxNjQ2MjQzMiwiZXhwIjoxNjUyNDYyNDMyLCJhdF9oYXNoIjoiV3c0YnlHU0tQQmkwWWdUMkFrWWdOQSIsIm5vbmNlIjoiYjAxUU55czUtN3JydDFCdk9tXzR2Y21MNjhUX1kzVW4ifQ.GFxHZpb-EAO0mpVd-u5hygo4EJnhNCeAsSQcWPfpcKs" \
https://s1kjjye3gi.execute-api.us-east-1.amazonaws.com/api/files/metadata

Frontend File Upload Web App URL:
http://file-upload-frontend-dev.us-east-1.elasticbeanstalk.com/
