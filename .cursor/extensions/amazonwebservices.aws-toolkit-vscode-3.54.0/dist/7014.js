"use strict";exports.id=7014,exports.ids=[7014],exports.modules={67014:(rt,pe,r)=>{r.d(pe,{GetRoleCredentialsCommand:()=>we,SSOClient:()=>tt});var $=r(34546),me=r(8029),n=r(93980);const ye=e=>({...e,useDualstackEndpoint:e.useDualstackEndpoint??!1,useFipsEndpoint:e.useFipsEndpoint??!1,defaultSigningName:"awsssoportal"}),ge={UseFIPS:{type:"builtInParams",name:"useFipsEndpoint"},Endpoint:{type:"builtInParams",name:"endpoint"},Region:{type:"builtInParams",name:"region"},UseDualStack:{type:"builtInParams",name:"useDualstackEndpoint"}};class p extends n.TJ{constructor(t){super(t),Object.setPrototypeOf(this,p.prototype)}}class A extends p{constructor(t){super({name:"InvalidRequestException",$fault:"client",...t}),this.name="InvalidRequestException",this.$fault="client",Object.setPrototypeOf(this,A.prototype)}}class T extends p{constructor(t){super({name:"ResourceNotFoundException",$fault:"client",...t}),this.name="ResourceNotFoundException",this.$fault="client",Object.setPrototypeOf(this,T.prototype)}}class w extends p{constructor(t){super({name:"TooManyRequestsException",$fault:"client",...t}),this.name="TooManyRequestsException",this.$fault="client",Object.setPrototypeOf(this,w.prototype)}}class k extends p{constructor(t){super({name:"UnauthorizedException",$fault:"client",...t}),this.name="UnauthorizedException",this.$fault="client",Object.setPrototypeOf(this,k.prototype)}}const Se=e=>({...e,...e.accessToken&&{accessToken:n.$H}}),ve=e=>({...e,...e.secretAccessKey&&{secretAccessKey:n.$H},...e.sessionToken&&{sessionToken:n.$H}}),fe=e=>({...e,...e.roleCredentials&&{roleCredentials:ve(e.roleCredentials)}}),it=e=>({...e,...e.accessToken&&{accessToken:SENSITIVE_STRING}}),dt=e=>({...e,...e.accessToken&&{accessToken:SENSITIVE_STRING}}),ct=e=>({...e,...e.accessToken&&{accessToken:SENSITIVE_STRING}});var F=r(75430),v=r(25158);const xe=async(e,t)=>{const s=(0,v.lI)(e,t),o=(0,n.Tj)({},n.eU,{[I]:e[E]});s.bp("/federation/credentials");const a=(0,n.Tj)({[Te]:[,(0,n.Y0)(e[Ae],"roleName")],[j]:[,(0,n.Y0)(e[L],"accountId")]});let i;return s.m("GET").h(o).q(a).b(i),s.build()},lt=async(e,t)=>{const s=rb(e,t),o=map({},isSerializableHeaderValue,{[I]:e[E]});s.bp("/assignment/roles");const a=map({[M]:[,e[U]],[G]:[()=>e.maxResults!==void 0,()=>e[H].toString()],[j]:[,__expectNonNull(e[L],"accountId")]});let i;return s.m("GET").h(o).q(a).b(i),s.build()},ut=async(e,t)=>{const s=rb(e,t),o=map({},isSerializableHeaderValue,{[I]:e[E]});s.bp("/assignment/accounts");const a=map({[M]:[,e[U]],[G]:[()=>e.maxResults!==void 0,()=>e[H].toString()]});let i;return s.m("GET").h(o).q(a).b(i),s.build()},ht=async(e,t)=>{const s=rb(e,t),o=map({},isSerializableHeaderValue,{[I]:e[E]});s.bp("/logout");let a;return s.m("POST").h(o).b(a),s.build()},Re=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return R(e,t);const s=(0,n.Tj)({$metadata:h(e)}),o=(0,n.Y0)((0,n.Xk)(await(0,F.Y2)(e.body,t)),"body"),a=(0,n.s)(o,{roleCredentials:n.Ss});return Object.assign(s,a),s},pt=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return R(e,t);const s=map({$metadata:h(e)}),o=__expectNonNull(__expectObject(await parseBody(e.body,t)),"body"),a=take(o,{nextToken:__expectString,roleList:_json});return Object.assign(s,a),s},mt=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return R(e,t);const s=map({$metadata:h(e)}),o=__expectNonNull(__expectObject(await parseBody(e.body,t)),"body"),a=take(o,{accountList:_json,nextToken:__expectString});return Object.assign(s,a),s},yt=async(e,t)=>{if(e.statusCode!==200&&e.statusCode>=300)return R(e,t);const s=map({$metadata:h(e)});return await collectBody(e.body,t),s},R=async(e,t)=>{const s={...e,body:await(0,F.CG)(e.body,t)},o=(0,F.cJ)(e,s.body);switch(o){case"InvalidRequestException":case"com.amazonaws.sso#InvalidRequestException":throw await Ie(s,t);case"ResourceNotFoundException":case"com.amazonaws.sso#ResourceNotFoundException":throw await Ce(s,t);case"TooManyRequestsException":case"com.amazonaws.sso#TooManyRequestsException":throw await Pe(s,t);case"UnauthorizedException":case"com.amazonaws.sso#UnauthorizedException":throw await be(s,t);default:const a=s.body;return Ee({output:e,parsedBody:a,errorCode:o})}},Ee=(0,n.jr)(p),Ie=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new A({$metadata:h(e),...s});return(0,n.Mw)(i,e.body)},Ce=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new T({$metadata:h(e),...s});return(0,n.Mw)(i,e.body)},Pe=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new w({$metadata:h(e),...s});return(0,n.Mw)(i,e.body)},be=async(e,t)=>{const s=(0,n.Tj)({}),o=e.body,a=(0,n.s)(o,{message:n.lK});Object.assign(s,a);const i=new k({$metadata:h(e),...s});return(0,n.Mw)(i,e.body)},h=e=>({httpStatusCode:e.statusCode,requestId:e.headers["x-amzn-requestid"]??e.headers["x-amzn-request-id"]??e.headers["x-amz-request-id"],extendedRequestId:e.headers["x-amz-id-2"],cfId:e.headers["x-amz-cf-id"]}),gt=(e,t)=>collectBody(e,t).then(s=>t.utf8Encoder(s)),L="accountId",E="accessToken",j="account_id",H="maxResults",G="max_result",U="nextToken",M="next_token",Ae="roleName",Te="role_name",I="x-amz-sso_bearer_token";class we extends n.uB.classBuilder().ep(ge).m(function(t,s,o,a){return[(0,me.TM)(o,this.serialize,this.deserialize),(0,$.rD)(o,t.getEndpointParameterInstructions())]}).s("SWBPortalService","GetRoleCredentials",{}).n("SSOClient","GetRoleCredentialsCommand").f(Se,fe).ser(xe).de(Re).build(){}var V=r(95758),ke=r(69914),Fe=r(88276),_=r(44984),f=r(57801),ze=r(51320),C=r(25263),De=r(19264),B=r(42952);const Ne=async(e,t,s)=>({operation:(0,B.u)(t).operation,region:await(0,B.t)(e.region)()||(()=>{throw new Error("expected `region` to be configured for `aws.auth#sigv4`")})()});function Oe(e){return{schemeId:"aws.auth#sigv4",signingProperties:{name:"awsssoportal",region:e.region},propertiesExtractor:(t,s)=>({signingProperties:{config:t,context:s}})}}function P(e){return{schemeId:"smithy.api#noAuth"}}const $e=e=>{const t=[];switch(e.operation){case"GetRoleCredentials":{t.push(P(e));break}case"ListAccountRoles":{t.push(P(e));break}case"ListAccounts":{t.push(P(e));break}case"Logout":{t.push(P(e));break}default:t.push(Oe(e))}return t},Le=e=>({...(0,De.h)(e)}),je={rE:"3.693.0"};var He=r(16227),K=r(18316),Ge=r(51461),m=r(75854),Z=r(32117),Ue=r(88226),Me=r(94134),Ve=r(69177),_e=r(42640),Y=r(61821),q=r(91908),Be=r(40279),z=r(5332);const J="required",d="fn",c="argv",y="ref",W=!0,X="isSet",x="booleanEquals",g="error",S="endpoint",u="tree",D="PartitionResult",N="getAttr",Q={[J]:!1,type:"String"},ee={[J]:!0,default:!1,type:"Boolean"},te={[y]:"Endpoint"},se={[d]:x,[c]:[{[y]:"UseFIPS"},!0]},ne={[d]:x,[c]:[{[y]:"UseDualStack"},!0]},l={},oe={[d]:N,[c]:[{[y]:D},"supportsFIPS"]},ae={[y]:D},re={[d]:x,[c]:[!0,{[d]:N,[c]:[ae,"supportsDualStack"]}]},ie=[se],de=[ne],ce=[{[y]:"Region"}],Ke={version:"1.0",parameters:{Region:Q,UseDualStack:ee,UseFIPS:ee,Endpoint:Q},rules:[{conditions:[{[d]:X,[c]:[te]}],rules:[{conditions:ie,error:"Invalid Configuration: FIPS and custom endpoint are not supported",type:g},{conditions:de,error:"Invalid Configuration: Dualstack and custom endpoint are not supported",type:g},{endpoint:{url:te,properties:l,headers:l},type:S}],type:u},{conditions:[{[d]:X,[c]:ce}],rules:[{conditions:[{[d]:"aws.partition",[c]:ce,assign:D}],rules:[{conditions:[se,ne],rules:[{conditions:[{[d]:x,[c]:[W,oe]},re],rules:[{endpoint:{url:"https://portal.sso-fips.{Region}.{PartitionResult#dualStackDnsSuffix}",properties:l,headers:l},type:S}],type:u},{error:"FIPS and DualStack are enabled, but this partition does not support one or both",type:g}],type:u},{conditions:ie,rules:[{conditions:[{[d]:x,[c]:[oe,W]}],rules:[{conditions:[{[d]:"stringEquals",[c]:[{[d]:N,[c]:[ae,"name"]},"aws-us-gov"]}],endpoint:{url:"https://portal.sso.{Region}.amazonaws.com",properties:l,headers:l},type:S},{endpoint:{url:"https://portal.sso-fips.{Region}.{PartitionResult#dnsSuffix}",properties:l,headers:l},type:S}],type:u},{error:"FIPS is enabled but this partition does not support FIPS",type:g}],type:u},{conditions:de,rules:[{conditions:[re],rules:[{endpoint:{url:"https://portal.sso.{Region}.{PartitionResult#dualStackDnsSuffix}",properties:l,headers:l},type:S}],type:u},{error:"DualStack is enabled but this partition does not support DualStack",type:g}],type:u},{endpoint:{url:"https://portal.sso.{Region}.{PartitionResult#dnsSuffix}",properties:l,headers:l},type:S}],type:u}],type:u},{error:"Invalid Configuration: Missing Region",type:g}]},Ze=new z.kS({size:50,params:["Endpoint","Region","UseDualStack","UseFIPS"]}),Ye=(e,t={})=>Ze.get(e,()=>(0,z.sO)(Ke,{endpointParams:e,logger:t.logger}));z.mw.aws=Be.UF;const qe=e=>({apiVersion:"2019-06-10",base64Decoder:e?.base64Decoder??Y.E,base64Encoder:e?.base64Encoder??Y.n,disableHostPrefix:e?.disableHostPrefix??!1,endpointProvider:e?.endpointProvider??Ye,extensions:e?.extensions??[],httpAuthSchemeProvider:e?.httpAuthSchemeProvider??$e,httpAuthSchemes:e?.httpAuthSchemes??[{schemeId:"aws.auth#sigv4",identityProvider:t=>t.getIdentityProvider("aws.auth#sigv4"),signer:new Ve.f2},{schemeId:"smithy.api#noAuth",identityProvider:t=>t.getIdentityProvider("smithy.api#noAuth")||(async()=>({})),signer:new v.mR}],logger:e?.logger??new n.N4,serviceId:e?.serviceId??"SSO",urlParser:e?.urlParser??_e.D,utf8Decoder:e?.utf8Decoder??q.ar,utf8Encoder:e?.utf8Encoder??q.Pq});var Je=r(12165);const We=e=>{(0,n.I9)(process.version);const t=(0,Je.I)(e),s=()=>t().then(n.lT),o=qe(e);return(0,He.I)(process.version),{...o,...e,runtime:"node",defaultsMode:t,bodyLengthChecker:e?.bodyLengthChecker??Ue.n,defaultUserAgentProvider:e?.defaultUserAgentProvider??(0,K.pf)({serviceId:o.serviceId,clientVersion:je.rE}),maxAttempts:e?.maxAttempts??(0,m.Z)(C.qs),region:e?.region??(0,m.Z)(f.GG,f.zH),requestHandler:Z.$c.create(e?.requestHandler??s),retryMode:e?.retryMode??(0,m.Z)({...C.kN,default:async()=>(await s()).retryMode||Me.L0}),sha256:e?.sha256??Ge.V.bind(null,"sha256"),streamCollector:e?.streamCollector??Z.kv,useDualstackEndpoint:e?.useDualstackEndpoint??(0,m.Z)(f.e$),useFipsEndpoint:e?.useFipsEndpoint??(0,m.Z)(f.Ko),userAgentAppId:e?.userAgentAppId??(0,m.Z)(K.hV)}};var le=r(91663),ue=r(90130);const Xe=e=>{const t=e.httpAuthSchemes;let s=e.httpAuthSchemeProvider,o=e.credentials;return{setHttpAuthScheme(a){const i=t.findIndex(O=>O.schemeId===a.schemeId);i===-1?t.push(a):t.splice(i,1,a)},httpAuthSchemes(){return t},setHttpAuthSchemeProvider(a){s=a},httpAuthSchemeProvider(){return s},setCredentials(a){o=a},credentials(){return o}}},Qe=e=>({httpAuthSchemes:e.httpAuthSchemes(),httpAuthSchemeProvider:e.httpAuthSchemeProvider(),credentials:e.credentials()}),b=e=>e,et=(e,t)=>{const s={...b((0,le.Rq)(e)),...b((0,n.xA)(e)),...b((0,ue.eS)(e)),...b(Xe(e))};return t.forEach(o=>o.configure(s)),{...e,...(0,le.$3)(s),...(0,n.uv)(s),...(0,ue.jt)(s),...Qe(s)}};class tt extends n.Kj{constructor(...[t]){const s=We(t||{}),o=ye(s),a=(0,_.Dc)(o),i=(0,C.$z)(a),O=(0,f.TD)(i),st=(0,V.OV)(O),nt=(0,$.Co)(st),ot=Le(nt),he=et(ot,t?.extensions||[]);super(he),this.config=he,this.middlewareStack.use((0,_.sM)(this.config)),this.middlewareStack.use((0,C.ey)(this.config)),this.middlewareStack.use((0,ze.vK)(this.config)),this.middlewareStack.use((0,V.TC)(this.config)),this.middlewareStack.use((0,ke.Y7)(this.config)),this.middlewareStack.use((0,Fe.n4)(this.config)),this.middlewareStack.use((0,v.wB)(this.config,{httpAuthSchemeParametersProvider:Ne,identityProviderConfigProvider:async at=>new v.h$({"aws.auth#sigv4":at.credentials})})),this.middlewareStack.use((0,v.lW)(this.config))}destroy(){super.destroy()}}}};
