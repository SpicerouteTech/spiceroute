"use strict";exports.id=8307,exports.ids=[8307],exports.modules={71295:(fe,L,r)=>{r.d(L,{CG:()=>n,Y2:()=>w,cJ:()=>N});var A=r(58362);const w=(g,c)=>(0,A.w)(g,c).then(l=>{if(l.length)try{return JSON.parse(l)}catch(m){throw m?.name==="SyntaxError"&&Object.defineProperty(m,"$responseBodyText",{value:l}),m}return{}}),n=async(g,c)=>{const l=await w(g,c);return l.message=l.message??l.Message,l},N=(g,c)=>{const l=(v,d)=>Object.keys(v).find(_=>_.toLowerCase()===d.toLowerCase()),m=v=>{let d=v;return typeof d=="number"&&(d=d.toString()),d.indexOf(",")>=0&&(d=d.split(",")[0]),d.indexOf(":")>=0&&(d=d.split(":")[0]),d.indexOf("#")>=0&&(d=d.split("#")[1]),d},f=l(g.headers,"x-amzn-errortype");if(f!==void 0)return m(g.headers[f]);if(c.code!==void 0)return m(c.code);if(c.__type!==void 0)return m(c.__type)}},58307:(fe,L,r)=>{r.d(L,{GetRoleCredentialsCommand:()=>Oe,SSOClient:()=>st});var A=r(34546),w=r(8029),n=r(93980);const N=e=>({...e,useDualstackEndpoint:e.useDualstackEndpoint??!1,useFipsEndpoint:e.useFipsEndpoint??!1,defaultSigningName:"awsssoportal"}),g={UseFIPS:{type:"builtInParams",name:"useFipsEndpoint"},Endpoint:{type:"builtInParams",name:"endpoint"},Region:{type:"builtInParams",name:"region"},UseDualStack:{type:"builtInParams",name:"useDualstackEndpoint"}};class c extends n.TJ{constructor(t){super(t),Object.setPrototypeOf(this,c.prototype)}}class l extends c{constructor(t){super({name:"InvalidRequestException",$fault:"client",...t}),this.name="InvalidRequestException",this.$fault="client",Object.setPrototypeOf(this,l.prototype)}}class m extends c{constructor(t){super({name:"ResourceNotFoundException",$fault:"client",...t}),this.name="ResourceNotFoundException",this.$fault="client",Object.setPrototypeOf(this,m.prototype)}}class f extends c{constructor(t){super({name:"TooManyRequestsException",$fault:"client",...t}),this.name="TooManyRequestsException",this.$fault="client",Object.setPrototypeOf(this,f.prototype)}}class v extends c{constructor(t){super({name:"UnauthorizedException",$fault:"client",...t}),this.name="UnauthorizedException",this.$fault="client",Object.setPrototypeOf(this,v.prototype)}}const d=e=>({...e,...e.accessToken&&{accessToken:n.$H}}),_=e=>({...e,...e.secretAccessKey&&{secretAccessKey:n.$H},...e.sessionToken&&{sessionToken:n.$H}}),xe=e=>({...e,...e.roleCredentials&&{roleCredentials:_(e.roleCredentials)}}),it=e=>({...e,...e.accessToken&&{accessToken:SENSITIVE_STRING}}),dt=e=>({...e,...e.accessToken&&{accessToken:SENSITIVE_STRING}}),ct=e=>({...e,...e.accessToken&&{accessToken:SENSITIVE_STRING}});var $=r(71295),I=r(25158);const Ee=async(e,t)=>{const s=(0,I.lI)(e,t),o=(0,n.Tj)({},n.eU,{[k]:e[O]});s.bp("/federation/credentials");const a=(0,n.Tj)({[Te]:[,(0,n.Y0)(e[we],"roleName")],[B]:[,(0,n.Y0)(e[U],"accountId")]});let i;return s.m("GET").h(o).q(a).b(i),s.build()},lt=async(e,t)=>{const s=rb(e,t),o=map({},isSerializableHeaderValue,{[k]:e[O]});s.bp("/assignment/roles");const a=map({[Y]:[,e[J]],[K]:[()=>e.maxResults!==void 0,()=>e[V].toString()],[B]:[,__expectNonNull(e[U],"accountId")]});let i;return s.m("GET").h(o).q(a).b(i),s.build()},ut=async(e,t)=>{const s=rb(e,t),o=map({},isSerializableHeaderValue,{[k]:e[O]});s.bp("/assignment/accounts");const a=map({[Y]:[,e[J]],[K]:[()=>e.maxResults!==void 0,()=>e[V].toString()]});let i;return s.m("GET").h(o).q(a).b(i),s.build()},ht=async(e,t)=>{const s=rb(e,t),o=map({},isSerializableHeaderValue,{[k]:e[O]});s.bp("/logout");let a;return s.m("POST").h(o).b(a),s.build()},Re=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return T(e,t);const s=(0,n.Tj)({$metadata:S(e)}),o=(0,n.Y0)((0,n.Xk)(await(0,$.Y2)(e.body,t)),"body"),a=(0,n.s)(o,{roleCredentials:n.Ss});return Object.assign(s,a),s},pt=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return T(e,t);const s=map({$metadata:S(e)}),o=__expectNonNull(__expectObject(await parseBody(e.body,t)),"body"),a=take(o,{nextToken:__expectString,roleList:_json});return Object.assign(s,a),s},mt=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return T(e,t);const s=map({$metadata:S(e)}),o=__expectNonNull(__expectObject(await parseBody(e.body,t)),"body"),a=take(o,{accountList:_json,nextToken:__expectString});return Object.assign(s,a),s},yt=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return T(e,t);const s=map({$metadata:S(e)});return await collectBody(e.body,t),s},T=async(e,t)=>{const s={...e,body:await(0,$.CG)(e.body,t)},o=(0,$.cJ)(e,s.body);switch(o){case"InvalidRequestException":case"com.amazonaws.sso#InvalidRequestException":throw await Ie(s,t);case"ResourceNotFoundException":case"com.amazonaws.sso#ResourceNotFoundException":throw await Pe(s,t);case"TooManyRequestsException":case"com.amazonaws.sso#TooManyRequestsException":throw await be(s,t);case"UnauthorizedException":case"com.amazonaws.sso#UnauthorizedException":throw await Ae(s,t);default:const a=s.body;return Ce({output:e,parsedBody:a,errorCode:o})}},Ce=(0,n.jr)(c),Ie=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new l({$metadata:S(e),...s});return(0,n.Mw)(i,e.body)},Pe=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new m({$metadata:S(e),...s});return(0,n.Mw)(i,e.body)},be=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new f({$metadata:S(e),...s});return(0,n.Mw)(i,e.body)},Ae=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new v({$metadata:S(e),...s});return(0,n.Mw)(i,e.body)},S=e=>({httpStatusCode:e.statusCode,requestId:e.headers["x-amzn-requestid"]??e.headers["x-amzn-request-id"]??e.headers["x-amz-request-id"],extendedRequestId:e.headers["x-amz-id-2"],cfId:e.headers["x-amz-cf-id"]}),gt=(e,t)=>collectBody(e,t).then(s=>t.utf8Encoder(s)),U="accountId",O="accessToken",B="account_id",V="maxResults",K="max_result",J="nextToken",Y="next_token",we="roleName",Te="role_name",k="x-amz-sso_bearer_token";class Oe extends n.uB.classBuilder().ep(g).m(function(t,s,o,a){return[(0,w.TM)(o,this.serialize,this.deserialize),(0,A.rD)(o,t.getEndpointParameterInstructions())]}).s("SWBPortalService","GetRoleCredentials",{}).n("SSOClient","GetRoleCredentialsCommand").f(d,xe).ser(Ee).de(Re).build(){}var Z=r(45703),ke=r(90111),ze=r(2649),W=r(16241),P=r(57801),De=r(51320),z=r(25263),Fe=r(44421),q=r(42952);const Le=async(e,t,s)=>({operation:(0,q.u)(t).operation,region:await(0,q.t)(e.region)()||(()=>{throw new Error("expected `region` to be configured for `aws.auth#sigv4`")})()});function Ne(e){return{schemeId:"aws.auth#sigv4",signingProperties:{name:"awsssoportal",region:e.region},propertiesExtractor:(t,s)=>({signingProperties:{config:t,context:s}})}}function D(e){return{schemeId:"smithy.api#noAuth"}}const _e=e=>{const t=[];switch(e.operation){case"GetRoleCredentials":{t.push(D(e));break}case"ListAccountRoles":{t.push(D(e));break}case"ListAccounts":{t.push(D(e));break}case"Logout":{t.push(D(e));break}default:t.push(Ne(e))}return t},$e=e=>({...(0,Fe.h)(e)}),je={rE:"3.693.0"};var He=r(45570),X=r(52039),Me=r(51461),x=r(75854),Q=r(32117),Ge=r(88226),Ue=r(94134),Be=r(93482),Ve=r(42640),ee=r(61821),te=r(82869),Ke=r(22780),j=r(5332);const se="required",u="fn",h="argv",E="ref",ne=!0,oe="isSet",b="booleanEquals",R="error",C="endpoint",y="tree",H="PartitionResult",M="getAttr",re={[se]:!1,type:"String"},ae={[se]:!0,default:!1,type:"Boolean"},ie={[E]:"Endpoint"},de={[u]:b,[h]:[{[E]:"UseFIPS"},!0]},ce={[u]:b,[h]:[{[E]:"UseDualStack"},!0]},p={},le={[u]:M,[h]:[{[E]:H},"supportsFIPS"]},ue={[E]:H},he={[u]:b,[h]:[!0,{[u]:M,[h]:[ue,"supportsDualStack"]}]},pe=[de],me=[ce],ye=[{[E]:"Region"}],Je={version:"1.0",parameters:{Region:re,UseDualStack:ae,UseFIPS:ae,Endpoint:re},rules:[{conditions:[{[u]:oe,[h]:[ie]}],rules:[{conditions:pe,error:"Invalid Configuration: FIPS and custom endpoint are not supported",type:R},{conditions:me,error:"Invalid Configuration: Dualstack and custom endpoint are not supported",type:R},{endpoint:{url:ie,properties:p,headers:p},type:C}],type:y},{conditions:[{[u]:oe,[h]:ye}],rules:[{conditions:[{[u]:"aws.partition",[h]:ye,assign:H}],rules:[{conditions:[de,ce],rules:[{conditions:[{[u]:b,[h]:[ne,le]},he],rules:[{endpoint:{url:"https://portal.sso-fips.{Region}.{PartitionResult#dualStackDnsSuffix}",properties:p,headers:p},type:C}],type:y},{error:"FIPS and DualStack are enabled, but this partition does not support one or both",type:R}],type:y},{conditions:pe,rules:[{conditions:[{[u]:b,[h]:[le,ne]}],rules:[{conditions:[{[u]:"stringEquals",[h]:[{[u]:M,[h]:[ue,"name"]},"aws-us-gov"]}],endpoint:{url:"https://portal.sso.{Region}.amazonaws.com",properties:p,headers:p},type:C},{endpoint:{url:"https://portal.sso-fips.{Region}.{PartitionResult#dnsSuffix}",properties:p,headers:p},type:C}],type:y},{error:"FIPS is enabled but this partition does not support FIPS",type:R}],type:y},{conditions:me,rules:[{conditions:[he],rules:[{endpoint:{url:"https://portal.sso.{Region}.{PartitionResult#dualStackDnsSuffix}",properties:p,headers:p},type:C}],type:y},{error:"DualStack is enabled but this partition does not support DualStack",type:R}],type:y},{endpoint:{url:"https://portal.sso.{Region}.{PartitionResult#dnsSuffix}",properties:p,headers:p},type:C}],type:y}],type:y},{error:"Invalid Configuration: Missing Region",type:R}]},Ye=new j.kS({size:50,params:["Endpoint","Region","UseDualStack","UseFIPS"]}),Ze=(e,t={})=>Ye.get(e,()=>(0,j.sO)(Je,{endpointParams:e,logger:t.logger}));j.mw.aws=Ke.UF;const We=e=>({apiVersion:"2019-06-10",base64Decoder:e?.base64Decoder??ee.E,base64Encoder:e?.base64Encoder??ee.n,disableHostPrefix:e?.disableHostPrefix??!1,endpointProvider:e?.endpointProvider??Ze,extensions:e?.extensions??[],httpAuthSchemeProvider:e?.httpAuthSchemeProvider??_e,httpAuthSchemes:e?.httpAuthSchemes??[{schemeId:"aws.auth#sigv4",identityProvider:t=>t.getIdentityProvider("aws.auth#sigv4"),signer:new Be.f2},{schemeId:"smithy.api#noAuth",identityProvider:t=>t.getIdentityProvider("smithy.api#noAuth")||(async()=>({})),signer:new I.mR}],logger:e?.logger??new n.N4,serviceId:e?.serviceId??"SSO",urlParser:e?.urlParser??Ve.D,utf8Decoder:e?.utf8Decoder??te.ar,utf8Encoder:e?.utf8Encoder??te.Pq});var qe=r(12165);const Xe=e=>{(0,n.I9)(process.version);const t=(0,qe.I)(e),s=()=>t().then(n.lT),o=We(e);return(0,He.I)(process.version),{...o,...e,runtime:"node",defaultsMode:t,bodyLengthChecker:e?.bodyLengthChecker??Ge.n,defaultUserAgentProvider:e?.defaultUserAgentProvider??(0,X.pf)({serviceId:o.serviceId,clientVersion:je.rE}),maxAttempts:e?.maxAttempts??(0,x.Z)(z.qs),region:e?.region??(0,x.Z)(P.GG,P.zH),requestHandler:Q.$c.create(e?.requestHandler??s),retryMode:e?.retryMode??(0,x.Z)({...z.kN,default:async()=>(await s()).retryMode||Ue.L0}),sha256:e?.sha256??Me.V.bind(null,"sha256"),streamCollector:e?.streamCollector??Q.kv,useDualstackEndpoint:e?.useDualstackEndpoint??(0,x.Z)(P.e$),useFipsEndpoint:e?.useFipsEndpoint??(0,x.Z)(P.Ko),userAgentAppId:e?.userAgentAppId??(0,x.Z)(X.hV)}};var ge=r(54848),Se=r(90130);const Qe=e=>{const t=e.httpAuthSchemes;let s=e.httpAuthSchemeProvider,o=e.credentials;return{setHttpAuthScheme(a){const i=t.findIndex(G=>G.schemeId===a.schemeId);i===-1?t.push(a):t.splice(i,1,a)},httpAuthSchemes(){return t},setHttpAuthSchemeProvider(a){s=a},httpAuthSchemeProvider(){return s},setCredentials(a){o=a},credentials(){return o}}},et=e=>({httpAuthSchemes:e.httpAuthSchemes(),httpAuthSchemeProvider:e.httpAuthSchemeProvider(),credentials:e.credentials()}),F=e=>e,tt=(e,t)=>{const s={...F((0,ge.Rq)(e)),...F((0,n.xA)(e)),...F((0,Se.eS)(e)),...F(Qe(e))};return t.forEach(o=>o.configure(s)),{...e,...(0,ge.$3)(s),...(0,n.uv)(s),...(0,Se.jt)(s),...et(s)}};class st extends n.Kj{constructor(...[t]){const s=Xe(t||{}),o=N(s),a=(0,W.Dc)(o),i=(0,z.$z)(a),G=(0,P.TD)(i),nt=(0,Z.OV)(G),ot=(0,A.Co)(nt),rt=$e(ot),ve=tt(rt,t?.extensions||[]);super(ve),this.config=ve,this.middlewareStack.use((0,W.sM)(this.config)),this.middlewareStack.use((0,z.ey)(this.config)),this.middlewareStack.use((0,De.vK)(this.config)),this.middlewareStack.use((0,Z.TC)(this.config)),this.middlewareStack.use((0,ke.Y7)(this.config)),this.middlewareStack.use((0,ze.n4)(this.config)),this.middlewareStack.use((0,I.wB)(this.config,{httpAuthSchemeParametersProvider:Le,identityProviderConfigProvider:async at=>new I.h$({"aws.auth#sigv4":at.credentials})})),this.middlewareStack.use((0,I.lW)(this.config))}destroy(){super.destroy()}}}};
