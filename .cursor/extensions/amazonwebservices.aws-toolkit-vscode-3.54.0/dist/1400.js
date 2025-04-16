"use strict";exports.id=1400,exports.ids=[1400],exports.modules={61400:(P,A,o)=>{o.d(A,{fromHttp:()=>K});var C=o(8818),l=o(32117),i=o(3631),I=o(91943),E=o.n(I);const k="127.0.0.0/8",D="::1/128",N="169.254.170.2",u="169.254.170.23",m="[fd00:ec2::23]",R=(e,s)=>{if(e.protocol!=="https:"&&!(e.hostname===N||e.hostname===u||e.hostname===m)){if(e.hostname.includes("[")){if(e.hostname==="[::1]"||e.hostname==="[0000:0000:0000:0000:0000:0000:0000:0001]")return}else{if(e.hostname==="localhost")return;const n=e.hostname.split("."),r=t=>{const a=parseInt(t,10);return 0<=a&&a<=255};if(n[0]==="127"&&r(n[1])&&r(n[2])&&r(n[3])&&n.length===4)return}throw new i.C1(`URL not accepted. It must either be HTTPS or match one of the following:
  - loopback CIDR 127.0.0.0/8 or [::1/128]
  - ECS container host 169.254.170.2
  - EKS container host 169.254.170.23 or [fd00:ec2::23]`,{logger:s})}};var g=o(90130),O=o(93980),S=o(26769);function f(e){return new g.Kd({protocol:e.protocol,hostname:e.hostname,port:Number(e.port),path:e.pathname,query:Array.from(e.searchParams.entries()).reduce((s,[n,r])=>(s[n]=r,s),{}),fragment:e.hash})}async function p(e,s){const r=await(0,S.c9)(e.body).transformToString();if(e.statusCode===200){const t=JSON.parse(r);if(typeof t.AccessKeyId!="string"||typeof t.SecretAccessKey!="string"||typeof t.Token!="string"||typeof t.Expiration!="string")throw new i.C1("HTTP credential provider response not of the required format, an object matching: { AccessKeyId: string, SecretAccessKey: string, Token: string, Expiration: string(rfc3339) }",{logger:s});return{accessKeyId:t.AccessKeyId,secretAccessKey:t.SecretAccessKey,sessionToken:t.Token,expiration:(0,O.EI)(t.Expiration)}}if(e.statusCode>=400&&e.statusCode<500){let t={};try{t=JSON.parse(r)}catch{}throw Object.assign(new i.C1(`Server responded with status: ${e.statusCode}`,{logger:s}),{Code:t.Code,Message:t.Message})}throw new i.C1(`Server responded with status: ${e.statusCode}`,{logger:s})}const w=(e,s,n)=>async()=>{for(let r=0;r<s;++r)try{return await e()}catch{await new Promise(a=>setTimeout(a,n))}return await e()},_="AWS_CONTAINER_CREDENTIALS_RELATIVE_URI",v="http://169.254.170.2",L="AWS_CONTAINER_CREDENTIALS_FULL_URI",y="AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE",U="AWS_CONTAINER_AUTHORIZATION_TOKEN",K=(e={})=>{e.logger?.debug("@aws-sdk/credential-provider-http - fromHttp");let s;const n=e.awsContainerCredentialsRelativeUri??process.env[_],r=e.awsContainerCredentialsFullUri??process.env[L],t=e.awsContainerAuthorizationToken??process.env[U],a=e.awsContainerAuthorizationTokenFile??process.env[y],c=e.logger?.constructor?.name==="NoOpLogger"||!e.logger?console.warn:e.logger.warn;if(n&&r&&(c("@aws-sdk/credential-provider-http: you have set both awsContainerCredentialsRelativeUri and awsContainerCredentialsFullUri."),c("awsContainerCredentialsFullUri will take precedence.")),t&&a&&(c("@aws-sdk/credential-provider-http: you have set both awsContainerAuthorizationToken and awsContainerAuthorizationTokenFile."),c("awsContainerAuthorizationToken will take precedence.")),r)s=r;else if(n)s=`${v}${n}`;else throw new i.C1(`No HTTP credential provider host provided.
Set AWS_CONTAINER_CREDENTIALS_FULL_URI or AWS_CONTAINER_CREDENTIALS_RELATIVE_URI.`,{logger:e.logger});const h=new URL(s);R(h,e.logger);const H=new l.$c({requestTimeout:e.timeout??1e3,connectionTimeout:e.timeout??1e3});return w(async()=>{const d=f(h);t?d.headers.Authorization=t:a&&(d.headers.Authorization=(await E().readFile(a)).toString());try{const T=await H.handle(d);return p(T.response).then(F=>(0,C.g)(F,"CREDENTIALS_HTTP","z"))}catch(T){throw new i.C1(String(T),{logger:e.logger})}},e.maxRetries??3,e.timeout??1e3)}}};
