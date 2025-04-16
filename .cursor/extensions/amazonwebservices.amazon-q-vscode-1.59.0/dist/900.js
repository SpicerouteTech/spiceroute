"use strict";exports.id=900,exports.ids=[900],exports.modules={8900:(Y,P,d)=>{d.d(P,{getInstanceMetadataEndpoint:()=>K,httpRequest:()=>w});var v=d(14904),ee=d(87016),D=d(20181),M=d(58611);function w(e){return new Promise((t,r)=>{const a=(0,M.request)({method:"GET",...e,hostname:e.hostname?.replace(/^\[(.+)\]$/,"$1")});a.on("error",n=>{r(Object.assign(new v.mZ("Unable to connect to instance metadata service"),n)),a.destroy()}),a.on("timeout",()=>{r(new v.mZ("TimeoutError from instance metadata service")),a.destroy()}),a.on("response",n=>{const{statusCode:l=400}=n;(l<200||300<=l)&&(r(Object.assign(new v.mZ("Error response received from instance metadata service"),{statusCode:l})),a.destroy());const u=[];n.on("data",o=>{u.push(o)}),n.on("end",()=>{t(D.Buffer.concat(u)),a.destroy()})}),a.end()})}const _="AWS_CONTAINER_CREDENTIALS_FULL_URI",h="AWS_CONTAINER_CREDENTIALS_RELATIVE_URI",A="AWS_CONTAINER_AUTHORIZATION_TOKEN",te=(e={})=>{const{timeout:t,maxRetries:r}=providerConfigFromInit(e);return()=>retry(async()=>{const a=await F({logger:e.logger}),n=JSON.parse(await y(t,a));if(!isImdsCredentials(n))throw new CredentialsProviderError("Invalid response received from instance metadata service.",{logger:e.logger});return fromImdsCredentials(n)},r)},y=async(e,t)=>(process.env[A]&&(t.headers={...t.headers,Authorization:process.env[A]}),(await httpRequest({...t,timeout:e})).toString()),b="169.254.170.2",R={localhost:!0,"127.0.0.1":!0},V={"http:":!0,"https:":!0},F=async({logger:e})=>{if(process.env[h])return{hostname:b,path:process.env[h]};if(process.env[_]){const t=parse(process.env[_]);if(!t.hostname||!(t.hostname in R))throw new CredentialsProviderError(`${t.hostname} is not a valid container metadata service hostname`,{tryNextLink:!1,logger:e});if(!t.protocol||!(t.protocol in V))throw new CredentialsProviderError(`${t.protocol} is not a valid container metadata service protocol`,{tryNextLink:!1,logger:e});return{...t,port:t.port?parseInt(t.port,10):void 0}}throw new CredentialsProviderError(`The container metadata credential provider cannot be used unless the ${h} or ${_} environment variable is set`,{tryNextLink:!1,logger:e})};var S=d(83995);class N extends v.C1{constructor(t,r=!0){super(t,r),this.tryNextLink=r,this.name="InstanceMetadataV1FallbackError",Object.setPrototypeOf(this,N.prototype)}}var k=d(89465),I;(function(e){e.IPv4="http://169.254.169.254",e.IPv6="http://[fd00:ec2::254]"})(I||(I={}));const L="AWS_EC2_METADATA_SERVICE_ENDPOINT",x="ec2_metadata_service_endpoint",W={environmentVariableSelector:e=>e[L],configFileSelector:e=>e[x],default:void 0};var f;(function(e){e.IPv4="IPv4",e.IPv6="IPv6"})(f||(f={}));const U="AWS_EC2_METADATA_SERVICE_ENDPOINT_MODE",$="ec2_metadata_service_endpoint_mode",G={environmentVariableSelector:e=>e[U],configFileSelector:e=>e[$],default:f.IPv4},K=async()=>(0,k.D)(await q()||await B()),q=async()=>(0,S.Z)(W)(),B=async()=>{const e=await(0,S.Z)(G)();switch(e){case f.IPv4:return I.IPv4;case f.IPv6:return I.IPv6;default:throw new Error(`Unsupported endpoint mode: ${e}. Select from ${Object.values(f)}`)}},C="/latest/meta-data/iam/security-credentials/",Z="/latest/api/token",g="AWS_EC2_METADATA_V1_DISABLED",T="ec2_metadata_v1_disabled",O="x-aws-ec2-metadata-token",ae=(e={})=>staticStabilityProvider(H(e),{logger:e.logger}),H=(e={})=>{let t=!1;const{logger:r,profile:a}=e,{timeout:n,maxRetries:l}=providerConfigFromInit(e),u=async(o,E)=>{if(t||E.headers?.[O]==null){let s=!1,i=!1;const Q=await loadConfig({environmentVariableSelector:c=>{const m=c[g];if(i=!!m&&m!=="false",m===void 0)throw new CredentialsProviderError(`${g} not set in env, checking config file next.`,{logger:e.logger});return i},configFileSelector:c=>{const m=c[T];return s=!!m&&m!=="false",s},default:!1},{profile:a})();if(e.ec2MetadataV1Disabled||Q){const c=[];throw e.ec2MetadataV1Disabled&&c.push("credential provider initialization (runtime option ec2MetadataV1Disabled)"),s&&c.push(`config file profile (${T})`),i&&c.push(`process environment variable (${g})`),new InstanceMetadataV1FallbackError(`AWS EC2 Metadata v1 fallback has been blocked by AWS SDK configuration in the following: [${c.join(", ")}].`)}}const X=(await retry(async()=>{let s;try{s=await z(E)}catch(i){throw i.statusCode===401&&(t=!1),i}return s},o)).trim();return retry(async()=>{let s;try{s=await J(X,E,e)}catch(i){throw i.statusCode===401&&(t=!1),i}return s},o)};return async()=>{const o=await getInstanceMetadataEndpoint();if(t)return r?.debug("AWS SDK Instance Metadata","using v1 fallback (no token fetch)"),u(l,{...o,timeout:n});{let E;try{E=(await j({...o,timeout:n})).toString()}catch(p){if(p?.statusCode===400)throw Object.assign(p,{message:"EC2 Metadata token request returned error"});return(p.message==="TimeoutError"||[403,404,405].includes(p.statusCode))&&(t=!0),r?.debug("AWS SDK Instance Metadata","using v1 fallback (initial)"),u(l,{...o,timeout:n})}return u(l,{...o,headers:{[O]:E},timeout:n})}}},j=async e=>httpRequest({...e,path:Z,method:"PUT",headers:{"x-aws-ec2-metadata-token-ttl-seconds":"21600"}}),z=async e=>(await httpRequest({...e,path:C})).toString(),J=async(e,t,r)=>{const a=JSON.parse((await httpRequest({...t,path:C+e})).toString());if(!isImdsCredentials(a))throw new CredentialsProviderError("Invalid response received from instance metadata service.",{logger:r.logger});return fromImdsCredentials(a)}}};
