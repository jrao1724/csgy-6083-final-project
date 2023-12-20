/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

var apigClientFactory = {};
apigClientFactory.newClient = function (config) {
    var apigClient = { };
    if(config === undefined) {
        config = {
            accessKey: '',
            secretKey: '',
            sessionToken: '',
            region: '',
            apiKey: undefined,
            defaultContentType: 'application/json',
            defaultAcceptType: 'application/json'
        };
    }
    if(config.accessKey === undefined) {
        config.accessKey = '';
    }
    if(config.secretKey === undefined) {
        config.secretKey = '';
    }
    if(config.apiKey === undefined) {
        config.apiKey = '';
    }
    if(config.sessionToken === undefined) {
        config.sessionToken = '';
    }
    if(config.region === undefined) {
        config.region = 'us-east-1';
    }
    //If defaultContentType is not defined then default to application/json
    if(config.defaultContentType === undefined) {
        config.defaultContentType = 'application/json';
    }
    //If defaultAcceptType is not defined then default to application/json
    if(config.defaultAcceptType === undefined) {
        config.defaultAcceptType = 'application/json';
    }

    
    // extract endpoint and path from url
    var invokeUrl = 'https://1d6a70nwfg.execute-api.us-east-1.amazonaws.com/Test1';
    var endpoint = /(^https?:\/\/[^\/]+)/g.exec(invokeUrl)[1];
    var pathComponent = invokeUrl.substring(endpoint.length);

    var sigV4ClientConfig = {
        accessKey: config.accessKey,
        secretKey: config.secretKey,
        sessionToken: config.sessionToken,
        serviceName: 'execute-api',
        region: config.region,
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var authType = 'NONE';
    if (sigV4ClientConfig.accessKey !== undefined && sigV4ClientConfig.accessKey !== '' && sigV4ClientConfig.secretKey !== undefined && sigV4ClientConfig.secretKey !== '') {
        authType = 'AWS_IAM';
    }

    var simpleHttpClientConfig = {
        endpoint: endpoint,
        defaultContentType: config.defaultContentType,
        defaultAcceptType: config.defaultAcceptType
    };

    var apiGatewayClient = apiGateway.core.apiGatewayClientFactory.newClient(simpleHttpClientConfig, sigV4ClientConfig);
    
    
    
    apigClient.createAccountPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var createAccountPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/createAccount').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(createAccountPostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.createAccountOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var createAccountOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/createAccount').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(createAccountOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.loginPost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['password', 'username'], ['body']);
        
        var loginPostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/login').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['password', 'username']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(loginPostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.loginOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var loginOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/login').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(loginOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['userName'], ['body']);
        
        var userNameGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}').expand(apiGateway.core.utils.parseParametersToObject(params, ['userName'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var userNameOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCreateCoursePost = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['userName', 'className'], ['body']);
        
        var userNameCreateCoursePostRequest = {
            verb: 'post'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/create-course').expand(apiGateway.core.utils.parseParametersToObject(params, ['userName', ])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, ['className']),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCreateCoursePostRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCreateCourseOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var userNameCreateCourseOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/create-course').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCreateCourseOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['courseName', 'userName'], ['body']);
        
        var userNameCourseNameGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}').expand(apiGateway.core.utils.parseParametersToObject(params, ['courseName', 'userName'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var userNameCourseNameOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameBigFileOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var userNameCourseNameBigFileOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}/bigFile').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameBigFileOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameBigFileFileNameGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['courseName', 'userName', 'fileName'], ['body']);
        
        var userNameCourseNameBigFileFileNameGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}/bigFile/{fileName}').expand(apiGateway.core.utils.parseParametersToObject(params, ['courseName', 'userName', 'fileName'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameBigFileFileNameGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameBigFileFileNameOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var userNameCourseNameBigFileFileNameOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}/bigFile/{fileName}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameBigFileFileNameOptionsRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameFileNameGet = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['courseName', 'userName', 'fileName'], ['body']);
        
        var userNameCourseNameFileNameGetRequest = {
            verb: 'get'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}/{fileName}').expand(apiGateway.core.utils.parseParametersToObject(params, ['courseName', 'userName', 'fileName'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameFileNameGetRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameFileNamePut = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, ['courseName', 'userName', 'fileName'], ['body']);
        
        var userNameCourseNameFileNamePutRequest = {
            verb: 'put'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}/{fileName}').expand(apiGateway.core.utils.parseParametersToObject(params, ['courseName', 'userName', 'fileName'])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameFileNamePutRequest, authType, additionalParams, config.apiKey);
    };
    
    
    apigClient.userNameCourseNameFileNameOptions = function (params, body, additionalParams) {
        if(additionalParams === undefined) { additionalParams = {}; }
        
        apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
        
        var userNameCourseNameFileNameOptionsRequest = {
            verb: 'options'.toUpperCase(),
            path: pathComponent + uritemplate('/{userName}/{courseName}/{fileName}').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
            headers: apiGateway.core.utils.parseParametersToObject(params, []),
            queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
            body: body
        };
        
        
        return apiGatewayClient.makeRequest(userNameCourseNameFileNameOptionsRequest, authType, additionalParams, config.apiKey);
    };
    

    return apigClient;
};
