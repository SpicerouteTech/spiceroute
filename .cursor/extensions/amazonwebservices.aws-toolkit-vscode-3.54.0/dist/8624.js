"use strict";exports.id=8624,exports.ids=[8624],exports.modules={38624:(m,l,o)=>{o.r(l),o.d(l,{fromTokenFile:()=>T,fromWebToken:()=>i});var a=o(45783),g=o(3631),E=o(79896);const i=e=>async()=>{e.logger?.debug("@aws-sdk/credential-provider-web-identity - fromWebToken");const{roleArn:n,roleSessionName:s,webIdentityToken:r,providerId:t,policyArns:y,policy:A,durationSeconds:I}=e;let{roleAssumerWithWebIdentity:d}=e;if(!d){const{getDefaultRoleAssumerWithWebIdentity:f}=await o.e(9863).then(o.bind(o,59863));d=f({...e.clientConfig,credentialProviderLogger:e.logger,parentClientConfig:e.parentClientConfig},e.clientPlugins)}return d({RoleArn:n,RoleSessionName:s??`aws-sdk-js-session-${Date.now()}`,WebIdentityToken:r,ProviderId:t,PolicyArns:y,Policy:A,DurationSeconds:I})},c="AWS_WEB_IDENTITY_TOKEN_FILE",S="AWS_ROLE_ARN",N="AWS_ROLE_SESSION_NAME",T=(e={})=>async()=>{e.logger?.debug("@aws-sdk/credential-provider-web-identity - fromTokenFile");const n=e?.webIdentityTokenFile??process.env[c],s=e?.roleArn??process.env[S],r=e?.roleSessionName??process.env[N];if(!n||!s)throw new g.C1("Web identity configuration not specified",{logger:e.logger});const t=await i({...e,webIdentityToken:(0,E.readFileSync)(n,{encoding:"ascii"}),roleArn:s,roleSessionName:r})();return n===process.env[c]&&(0,a.g)(t,"CREDENTIALS_ENV_VARS_STS_WEB_ID_TOKEN","h"),t}}};
