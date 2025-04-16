"use strict";exports.id=5869,exports.ids=[5869],exports.modules={35869:(xn,Vs,d)=>{d.d(Vs,{getDefaultRoleAssumer:()=>Ns,getDefaultRoleAssumerWithWebIdentity:()=>Bs});var ce=d(48166),ae=d(34546),ss=d(8029),r=d(93980);const Zs=e=>({...e,useDualstackEndpoint:e.useDualstackEndpoint??!1,useFipsEndpoint:e.useFipsEndpoint??!1,useGlobalEndpoint:e.useGlobalEndpoint??!1,defaultSigningName:"sts"}),ts={UseGlobalEndpoint:{type:"builtInParams",name:"useGlobalEndpoint"},UseFIPS:{type:"builtInParams",name:"useFipsEndpoint"},Endpoint:{type:"builtInParams",name:"endpoint"},Region:{type:"builtInParams",name:"region"},UseDualStack:{type:"builtInParams",name:"useDualstackEndpoint"}};class _ extends r.TJ{constructor(t){super(t),Object.setPrototypeOf(this,_.prototype)}}class de extends _{constructor(t){super({name:"ExpiredTokenException",$fault:"client",...t}),this.name="ExpiredTokenException",this.$fault="client",Object.setPrototypeOf(this,de.prototype)}}class le extends _{constructor(t){super({name:"MalformedPolicyDocumentException",$fault:"client",...t}),this.name="MalformedPolicyDocumentException",this.$fault="client",Object.setPrototypeOf(this,le.prototype)}}class me extends _{constructor(t){super({name:"PackedPolicyTooLargeException",$fault:"client",...t}),this.name="PackedPolicyTooLargeException",this.$fault="client",Object.setPrototypeOf(this,me.prototype)}}class ue extends _{constructor(t){super({name:"RegionDisabledException",$fault:"client",...t}),this.name="RegionDisabledException",this.$fault="client",Object.setPrototypeOf(this,ue.prototype)}}class fe extends _{constructor(t){super({name:"IDPRejectedClaimException",$fault:"client",...t}),this.name="IDPRejectedClaimException",this.$fault="client",Object.setPrototypeOf(this,fe.prototype)}}class he extends _{constructor(t){super({name:"InvalidIdentityTokenException",$fault:"client",...t}),this.name="InvalidIdentityTokenException",this.$fault="client",Object.setPrototypeOf(this,he.prototype)}}class ye extends _{constructor(t){super({name:"IDPCommunicationErrorException",$fault:"client",...t}),this.name="IDPCommunicationErrorException",this.$fault="client",Object.setPrototypeOf(this,ye.prototype)}}class ge extends _{constructor(t){super({name:"InvalidAuthorizationMessageException",$fault:"client",...t}),this.name="InvalidAuthorizationMessageException",this.$fault="client",Object.setPrototypeOf(this,ge.prototype)}}const H=e=>({...e,...e.SecretAccessKey&&{SecretAccessKey:r.$H}}),Qs=e=>({...e,...e.Credentials&&{Credentials:H(e.Credentials)}}),Tn=e=>({...e,...e.SAMLAssertion&&{SAMLAssertion:SENSITIVE_STRING}}),wn=e=>({...e,...e.Credentials&&{Credentials:H(e.Credentials)}}),qs=e=>({...e,...e.WebIdentityToken&&{WebIdentityToken:r.$H}}),Js=e=>({...e,...e.Credentials&&{Credentials:H(e.Credentials)}}),Dn=e=>({...e,...e.Credentials&&{Credentials:H(e.Credentials)}}),$n=e=>({...e,...e.Credentials&&{Credentials:H(e.Credentials)}}),Wn=e=>({...e,...e.Credentials&&{Credentials:H(e.Credentials)}});var Ae=d(63247),Se=d(90130);const Ys=async(e,t)=>{const s=$;let n;return n=L({...lt(e,t),[M]:Ot,[F]:W}),D(t,s,"/",void 0,n)},Mn=async(e,t)=>{const s=$;let n;return n=L({...mt(e,t),[M]:Ht,[F]:W}),D(t,s,"/",void 0,n)},Xs=async(e,t)=>{const s=$;let n;return n=L({...ut(e,t),[M]:jt,[F]:W}),D(t,s,"/",void 0,n)},kn=async(e,t)=>{const s=$;let n;return n=L({...ft(e,t),[M]:Nt,[F]:W}),D(t,s,"/",void 0,n)},Kn=async(e,t)=>{const s=$;let n;return n=L({...ht(e,t),[M]:Bt,[F]:W}),D(t,s,"/",void 0,n)},zn=async(e,t)=>{const s=$;let n;return n=L({...yt(e,t),[M]:Vt,[F]:W}),D(t,s,"/",void 0,n)},Fn=async(e,t)=>{const s=$;let n;return n=L({...gt(e,t),[M]:Zt,[F]:W}),D(t,s,"/",void 0,n)},Ln=async(e,t)=>{const s=$;let n;return n=L({...At(e,t),[M]:Qt,[F]:W}),D(t,s,"/",void 0,n)},Gn=async(e,t)=>{const s=$;let n;return n=L({...St(e,t),[M]:qt,[F]:W}),D(t,s,"/",void 0,n)},et=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await(0,Ae.t_)(e.body,t);let n={};return n=Pt(s.AssumeRoleResult,t),{$metadata:g(e),...n}},Un=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await parseBody(e.body,t);let n={};return n=vt(s.AssumeRoleWithSAMLResult,t),{$metadata:g(e),...n}},st=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await(0,Ae.t_)(e.body,t);let n={};return n=pt(s.AssumeRoleWithWebIdentityResult,t),{$metadata:g(e),...n}},On=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await parseBody(e.body,t);let n={};return n=_t(s.AssumeRootResult,t),{$metadata:g(e),...n}},Hn=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await parseBody(e.body,t);let n={};return n=bt(s.DecodeAuthorizationMessageResult,t),{$metadata:g(e),...n}},jn=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await parseBody(e.body,t);let n={};return n=wt(s.GetAccessKeyInfoResult,t),{$metadata:g(e),...n}},Nn=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await parseBody(e.body,t);let n={};return n=Dt(s.GetCallerIdentityResult,t),{$metadata:g(e),...n}},Bn=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await parseBody(e.body,t);let n={};return n=$t(s.GetFederationTokenResult,t),{$metadata:g(e),...n}},Vn=async(e,t)=>{if(e.statusCode>=300)return w(e,t);const s=await parseBody(e.body,t);let n={};return n=Wt(s.GetSessionTokenResult,t),{$metadata:g(e),...n}},w=async(e,t)=>{const s={...e,body:await(0,Ae.FI)(e.body,t)},n=Jt(e,s.body);switch(n){case"ExpiredTokenException":case"com.amazonaws.sts#ExpiredTokenException":throw await tt(s,t);case"MalformedPolicyDocument":case"com.amazonaws.sts#MalformedPolicyDocumentException":throw await ct(s,t);case"PackedPolicyTooLarge":case"com.amazonaws.sts#PackedPolicyTooLargeException":throw await at(s,t);case"RegionDisabledException":case"com.amazonaws.sts#RegionDisabledException":throw await dt(s,t);case"IDPRejectedClaim":case"com.amazonaws.sts#IDPRejectedClaimException":throw await ot(s,t);case"InvalidIdentityToken":case"com.amazonaws.sts#InvalidIdentityTokenException":throw await it(s,t);case"IDPCommunicationError":case"com.amazonaws.sts#IDPCommunicationErrorException":throw await nt(s,t);case"InvalidAuthorizationMessageException":case"com.amazonaws.sts#InvalidAuthorizationMessageException":throw await rt(s,t);default:const o=s.body;return Ut({output:e,parsedBody:o.Error,errorCode:n})}},tt=async(e,t)=>{const s=e.body,n=xt(s.Error,t),o=new de({$metadata:g(e),...n});return(0,r.Mw)(o,s)},nt=async(e,t)=>{const s=e.body,n=Mt(s.Error,t),o=new ye({$metadata:g(e),...n});return(0,r.Mw)(o,s)},ot=async(e,t)=>{const s=e.body,n=kt(s.Error,t),o=new fe({$metadata:g(e),...n});return(0,r.Mw)(o,s)},rt=async(e,t)=>{const s=e.body,n=Kt(s.Error,t),o=new ge({$metadata:g(e),...n});return(0,r.Mw)(o,s)},it=async(e,t)=>{const s=e.body,n=zt(s.Error,t),o=new he({$metadata:g(e),...n});return(0,r.Mw)(o,s)},ct=async(e,t)=>{const s=e.body,n=Ft(s.Error,t),o=new le({$metadata:g(e),...n});return(0,r.Mw)(o,s)},at=async(e,t)=>{const s=e.body,n=Lt(s.Error,t),o=new me({$metadata:g(e),...n});return(0,r.Mw)(o,s)},dt=async(e,t)=>{const s=e.body,n=Gt(s.Error,t),o=new ue({$metadata:g(e),...n});return(0,r.Mw)(o,s)},lt=(e,t)=>{const s={};if(e[z]!=null&&(s[z]=e[z]),e[Z]!=null&&(s[Z]=e[Z]),e[v]!=null){const n=ne(e[v],t);e[v]?.length===0&&(s.PolicyArns=[]),Object.entries(n).forEach(([o,a])=>{const i=`PolicyArns.${o}`;s[i]=a})}if(e[P]!=null&&(s[P]=e[P]),e[y]!=null&&(s[y]=e[y]),e[q]!=null){const n=os(e[q],t);e[q]?.length===0&&(s.Tags=[]),Object.entries(n).forEach(([o,a])=>{const i=`Tags.${o}`;s[i]=a})}if(e[je]!=null){const n=Ct(e[je],t);e[je]?.length===0&&(s.TransitiveTagKeys=[]),Object.entries(n).forEach(([o,a])=>{const i=`TransitiveTagKeys.${o}`;s[i]=a})}if(e[ve]!=null&&(s[ve]=e[ve]),e[Q]!=null&&(s[Q]=e[Q]),e[J]!=null&&(s[J]=e[J]),e[E]!=null&&(s[E]=e[E]),e[Me]!=null){const n=Et(e[Me],t);e[Me]?.length===0&&(s.ProvidedContexts=[]),Object.entries(n).forEach(([o,a])=>{const i=`ProvidedContexts.${o}`;s[i]=a})}return s},mt=(e,t)=>{const s={};if(e[z]!=null&&(s[z]=e[z]),e[$e]!=null&&(s[$e]=e[$e]),e[Le]!=null&&(s[Le]=e[Le]),e[v]!=null){const n=ne(e[v],t);e[v]?.length===0&&(s.PolicyArns=[]),Object.entries(n).forEach(([o,a])=>{const i=`PolicyArns.${o}`;s[i]=a})}return e[P]!=null&&(s[P]=e[P]),e[y]!=null&&(s[y]=e[y]),s},ut=(e,t)=>{const s={};if(e[z]!=null&&(s[z]=e[z]),e[Z]!=null&&(s[Z]=e[Z]),e[Ve]!=null&&(s[Ve]=e[Ve]),e[ke]!=null&&(s[ke]=e[ke]),e[v]!=null){const n=ne(e[v],t);e[v]?.length===0&&(s.PolicyArns=[]),Object.entries(n).forEach(([o,a])=>{const i=`PolicyArns.${o}`;s[i]=a})}return e[P]!=null&&(s[P]=e[P]),e[y]!=null&&(s[y]=e[y]),s},ft=(e,t)=>{const s={};if(e[He]!=null&&(s[He]=e[He]),e[rs]!=null){const n=ns(e[rs],t);Object.entries(n).forEach(([o,a])=>{const i=`TaskPolicyArn.${o}`;s[i]=a})}return e[y]!=null&&(s[y]=e[y]),s},ht=(e,t)=>{const s={};return e[pe]!=null&&(s[pe]=e[pe]),s},yt=(e,t)=>{const s={};return e[N]!=null&&(s[N]=e[N]),s},gt=(e,t)=>({}),At=(e,t)=>{const s={};if(e[we]!=null&&(s[we]=e[we]),e[P]!=null&&(s[P]=e[P]),e[v]!=null){const n=ne(e[v],t);e[v]?.length===0&&(s.PolicyArns=[]),Object.entries(n).forEach(([o,a])=>{const i=`PolicyArns.${o}`;s[i]=a})}if(e[y]!=null&&(s[y]=e[y]),e[q]!=null){const n=os(e[q],t);e[q]?.length===0&&(s.Tags=[]),Object.entries(n).forEach(([o,a])=>{const i=`Tags.${o}`;s[i]=a})}return s},St=(e,t)=>{const s={};return e[y]!=null&&(s[y]=e[y]),e[Q]!=null&&(s[Q]=e[Q]),e[J]!=null&&(s[J]=e[J]),s},ne=(e,t)=>{const s={};let n=1;for(const o of e){if(o===null)continue;const a=ns(o,t);Object.entries(a).forEach(([i,I])=>{s[`member.${n}.${i}`]=I}),n++}return s},ns=(e,t)=>{const s={};return e[Ze]!=null&&(s[Ze]=e[Ze]),s},Rt=(e,t)=>{const s={};return e[We]!=null&&(s[We]=e[We]),e[Ie]!=null&&(s[Ie]=e[Ie]),s},Et=(e,t)=>{const s={};let n=1;for(const o of e){if(o===null)continue;const a=Rt(o,t);Object.entries(a).forEach(([i,I])=>{s[`member.${n}.${i}`]=I}),n++}return s},It=(e,t)=>{const s={};return e[Te]!=null&&(s[Te]=e[Te]),e[Be]!=null&&(s[Be]=e[Be]),s},Ct=(e,t)=>{const s={};let n=1;for(const o of e)o!==null&&(s[`member.${n}`]=o,n++);return s},os=(e,t)=>{const s={};let n=1;for(const o of e){if(o===null)continue;const a=It(o,t);Object.entries(a).forEach(([i,I])=>{s[`member.${n}.${i}`]=I}),n++}return s},Re=(e,t)=>{const s={};return e[Ee]!=null&&(s[Ee]=(0,r.lK)(e[Ee])),e[K]!=null&&(s[K]=(0,r.lK)(e[K])),s},Pt=(e,t)=>{const s={};return e[h]!=null&&(s[h]=j(e[h],t)),e[k]!=null&&(s[k]=Re(e[k],t)),e[p]!=null&&(s[p]=(0,r.xW)(e[p])),e[E]!=null&&(s[E]=(0,r.lK)(e[E])),s},vt=(e,t)=>{const s={};return e[h]!=null&&(s[h]=j(e[h],t)),e[k]!=null&&(s[k]=Re(e[k],t)),e[p]!=null&&(s[p]=__strictParseInt32(e[p])),e[ze]!=null&&(s[ze]=__expectString(e[ze])),e[Ue]!=null&&(s[Ue]=__expectString(e[Ue])),e[xe]!=null&&(s[xe]=__expectString(e[xe])),e[V]!=null&&(s[V]=__expectString(e[V])),e[De]!=null&&(s[De]=__expectString(e[De])),e[E]!=null&&(s[E]=__expectString(e[E])),s},pt=(e,t)=>{const s={};return e[h]!=null&&(s[h]=j(e[h],t)),e[Ge]!=null&&(s[Ge]=(0,r.lK)(e[Ge])),e[k]!=null&&(s[k]=Re(e[k],t)),e[p]!=null&&(s[p]=(0,r.xW)(e[p])),e[Ke]!=null&&(s[Ke]=(0,r.lK)(e[Ke])),e[V]!=null&&(s[V]=(0,r.lK)(e[V])),e[E]!=null&&(s[E]=(0,r.lK)(e[E])),s},_t=(e,t)=>{const s={};return e[h]!=null&&(s[h]=j(e[h],t)),e[E]!=null&&(s[E]=__expectString(e[E])),s},j=(e,t)=>{const s={};return e[N]!=null&&(s[N]=(0,r.lK)(e[N])),e[Fe]!=null&&(s[Fe]=(0,r.lK)(e[Fe])),e[Oe]!=null&&(s[Oe]=(0,r.lK)(e[Oe])),e[Pe]!=null&&(s[Pe]=(0,r.Y0)((0,r.t_)(e[Pe]))),s},bt=(e,t)=>{const s={};return e[Ce]!=null&&(s[Ce]=__expectString(e[Ce])),s},xt=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},Tt=(e,t)=>{const s={};return e[be]!=null&&(s[be]=__expectString(e[be])),e[K]!=null&&(s[K]=__expectString(e[K])),s},wt=(e,t)=>{const s={};return e[B]!=null&&(s[B]=__expectString(e[B])),s},Dt=(e,t)=>{const s={};return e[Ne]!=null&&(s[Ne]=__expectString(e[Ne])),e[B]!=null&&(s[B]=__expectString(e[B])),e[K]!=null&&(s[K]=__expectString(e[K])),s},$t=(e,t)=>{const s={};return e[h]!=null&&(s[h]=j(e[h],t)),e[_e]!=null&&(s[_e]=Tt(e[_e],t)),e[p]!=null&&(s[p]=__strictParseInt32(e[p])),s},Wt=(e,t)=>{const s={};return e[h]!=null&&(s[h]=j(e[h],t)),s},Mt=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},kt=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},Kt=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},zt=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},Ft=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},Lt=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},Gt=(e,t)=>{const s={};return e[u]!=null&&(s[u]=(0,r.lK)(e[u])),s},g=e=>({httpStatusCode:e.statusCode,requestId:e.headers["x-amzn-requestid"]??e.headers["x-amzn-request-id"]??e.headers["x-amz-request-id"],extendedRequestId:e.headers["x-amz-id-2"],cfId:e.headers["x-amz-cf-id"]}),Zn=(e,t)=>collectBody(e,t).then(s=>t.utf8Encoder(s)),Ut=(0,r.jr)(_),D=async(e,t,s,n,o)=>{const{hostname:a,protocol:i="https",port:I,path:x}=await e.endpoint(),T={protocol:i,hostname:a,port:I,method:"POST",path:x.endsWith("/")?x.slice(0,-1)+s:x+s,headers:t};return n!==void 0&&(T.hostname=n),o!==void 0&&(T.body=o),new Se.Kd(T)},$={"content-type":"application/x-www-form-urlencoded"},W="2011-06-15",M="Action",N="AccessKeyId",Ot="AssumeRole",Ee="AssumedRoleId",k="AssumedRoleUser",Ht="AssumeRoleWithSAML",jt="AssumeRoleWithWebIdentity",Nt="AssumeRoot",B="Account",K="Arn",V="Audience",h="Credentials",Ie="ContextAssertion",Bt="DecodeAuthorizationMessage",Ce="DecodedMessage",y="DurationSeconds",Pe="Expiration",ve="ExternalId",pe="EncodedMessage",_e="FederatedUser",be="FederatedUserId",Vt="GetAccessKeyInfo",Zt="GetCallerIdentity",Qt="GetFederationToken",qt="GetSessionToken",xe="Issuer",Te="Key",we="Name",De="NameQualifier",P="Policy",v="PolicyArns",$e="PrincipalArn",We="ProviderArn",Me="ProvidedContexts",ke="ProviderId",p="PackedPolicySize",Ke="Provider",z="RoleArn",Z="RoleSessionName",ze="Subject",Fe="SecretAccessKey",Le="SAMLAssertion",Ge="SubjectFromWebIdentityToken",E="SourceIdentity",Q="SerialNumber",Ue="SubjectType",Oe="SessionToken",q="Tags",J="TokenCode",He="TargetPrincipal",rs="TaskPolicyArn",je="TransitiveTagKeys",Ne="UserId",F="Version",Be="Value",Ve="WebIdentityToken",Ze="arn",u="message",L=e=>Object.entries(e).map(([t,s])=>(0,r.$6)(t)+"="+(0,r.$6)(s)).join("&"),Jt=(e,t)=>{if(t.Error?.Code!==void 0)return t.Error.Code;if(e.statusCode==404)return"NotFound"};class Yt extends r.uB.classBuilder().ep(ts).m(function(t,s,n,o){return[(0,ss.TM)(n,this.serialize,this.deserialize),(0,ae.rD)(n,t.getEndpointParameterInstructions())]}).s("AWSSecurityTokenServiceV20110615","AssumeRole",{}).n("STSClient","AssumeRoleCommand").f(void 0,Qs).ser(Ys).de(et).build(){}class Xt extends r.uB.classBuilder().ep(ts).m(function(t,s,n,o){return[(0,ss.TM)(n,this.serialize,this.deserialize),(0,ae.rD)(n,t.getEndpointParameterInstructions())]}).s("AWSSecurityTokenServiceV20110615","AssumeRoleWithWebIdentity",{}).n("STSClient","AssumeRoleWithWebIdentityCommand").f(qs,Js).ser(Xs).de(st).build(){}const is="us-east-1",cs=e=>{if(typeof e?.Arn=="string"){const t=e.Arn.split(":");if(t.length>4&&t[4]!=="")return t[4]}},as=async(e,t,s)=>{const n=typeof e=="function"?await e():e,o=typeof t=="function"?await t():t;return s?.debug?.("@aws-sdk/client-sts::resolveRegion","accepting first of:",`${n} (provider)`,`${o} (parent client)`,`${is} (STS default)`),n??o??is},ds=(e,t)=>{let s,n;return async(o,a)=>{if(n=o,!s){const{logger:O=e?.parentClientConfig?.logger,region:te,requestHandler:ie=e?.parentClientConfig?.requestHandler,credentialProviderLogger:es}=e,_n=await as(te,e?.parentClientConfig?.region,es),bn=!ms(ie);s=new t({credentialDefaultProvider:()=>async()=>n,region:_n,requestHandler:bn?ie:void 0,logger:O})}const{Credentials:i,AssumedRoleUser:I}=await s.send(new Yt(a));if(!i||!i.AccessKeyId||!i.SecretAccessKey)throw new Error(`Invalid response from STS.assumeRole call with role ${a.RoleArn}`);const x=cs(I),T={accessKeyId:i.AccessKeyId,secretAccessKey:i.SecretAccessKey,sessionToken:i.SessionToken,expiration:i.Expiration,...i.CredentialScope&&{credentialScope:i.CredentialScope},...x&&{accountId:x}};return(0,ce.g)(T,"CREDENTIALS_STS_ASSUME_ROLE","i"),T}},ls=(e,t)=>{let s;return async n=>{if(!s){const{logger:x=e?.parentClientConfig?.logger,region:T,requestHandler:O=e?.parentClientConfig?.requestHandler,credentialProviderLogger:te}=e,ie=await as(T,e?.parentClientConfig?.region,te),es=!ms(O);s=new t({region:ie,requestHandler:es?O:void 0,logger:x})}const{Credentials:o,AssumedRoleUser:a}=await s.send(new Xt(n));if(!o||!o.AccessKeyId||!o.SecretAccessKey)throw new Error(`Invalid response from STS.assumeRoleWithWebIdentity call with role ${n.RoleArn}`);const i=cs(a),I={accessKeyId:o.AccessKeyId,secretAccessKey:o.SecretAccessKey,sessionToken:o.SessionToken,expiration:o.Expiration,...o.CredentialScope&&{credentialScope:o.CredentialScope},...i&&{accountId:i}};return i&&(0,ce.g)(I,"RESOLVED_ACCOUNT_ID","T"),(0,ce.g)(I,"CREDENTIALS_STS_ASSUME_ROLE_WEB_ID","k"),I}},Qn=e=>t=>e({roleAssumer:ds(t,t.stsClientCtor),roleAssumerWithWebIdentity:ls(t,t.stsClientCtor),...t}),ms=e=>e?.metadata?.handlerProtocol==="h2";var us=d(74977),en=d(16017),sn=d(2115),fs=d(47235),ee=d(57801),se=d(25158),tn=d(51320),oe=d(25263),nn=d(9087),hs=d(42952);const on=async(e,t,s)=>({operation:(0,hs.u)(t).operation,region:await(0,hs.t)(e.region)()||(()=>{throw new Error("expected `region` to be configured for `aws.auth#sigv4`")})()});function rn(e){return{schemeId:"aws.auth#sigv4",signingProperties:{name:"sts",region:e.region},propertiesExtractor:(t,s)=>({signingProperties:{config:t,context:s}})}}function ys(e){return{schemeId:"smithy.api#noAuth"}}const cn=e=>{const t=[];switch(e.operation){case"AssumeRoleWithSAML":{t.push(ys(e));break}case"AssumeRoleWithWebIdentity":{t.push(ys(e));break}default:t.push(rn(e))}return t},an=e=>({...e,stsClientCtor:Xe}),dn=e=>{const t=an(e);return{...(0,nn.h)(t)}},ln={rE:"3.693.0"};var mn=d(15044),gs=d(24878),As=d(49699),Ss=d(43441),un=d(51461),Y=d(75854),Rs=d(32117),fn=d(88226),hn=d(94134),yn=d(42640),Es=d(61821),Is=d(52807),gn=d(52370),Qe=d(5332);const Cs="required",c="type",l="fn",m="argv",G="ref",Ps=!1,qe=!0,U="booleanEquals",A="stringEquals",vs="sigv4",ps="sts",_s="us-east-1",f="endpoint",bs="https://sts.{Region}.{PartitionResult#dnsSuffix}",b="tree",X="error",Je="getAttr",xs={[Cs]:!1,[c]:"String"},Ye={[Cs]:!0,default:!1,[c]:"Boolean"},Ts={[G]:"Endpoint"},ws={[l]:"isSet",[m]:[{[G]:"Region"}]},S={[G]:"Region"},Ds={[l]:"aws.partition",[m]:[S],assign:"PartitionResult"},$s={[G]:"UseFIPS"},Ws={[G]:"UseDualStack"},R={url:"https://sts.amazonaws.com",properties:{authSchemes:[{name:vs,signingName:ps,signingRegion:_s}]},headers:{}},C={},Ms={conditions:[{[l]:A,[m]:[S,"aws-global"]}],[f]:R,[c]:f},ks={[l]:U,[m]:[$s,!0]},Ks={[l]:U,[m]:[Ws,!0]},zs={[l]:Je,[m]:[{[G]:"PartitionResult"},"supportsFIPS"]},Fs={[G]:"PartitionResult"},Ls={[l]:U,[m]:[!0,{[l]:Je,[m]:[Fs,"supportsDualStack"]}]},Gs=[{[l]:"isSet",[m]:[Ts]}],Us=[ks],Os=[Ks],An={version:"1.0",parameters:{Region:xs,UseDualStack:Ye,UseFIPS:Ye,Endpoint:xs,UseGlobalEndpoint:Ye},rules:[{conditions:[{[l]:U,[m]:[{[G]:"UseGlobalEndpoint"},qe]},{[l]:"not",[m]:Gs},ws,Ds,{[l]:U,[m]:[$s,Ps]},{[l]:U,[m]:[Ws,Ps]}],rules:[{conditions:[{[l]:A,[m]:[S,"ap-northeast-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"ap-south-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"ap-southeast-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"ap-southeast-2"]}],endpoint:R,[c]:f},Ms,{conditions:[{[l]:A,[m]:[S,"ca-central-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"eu-central-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"eu-north-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"eu-west-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"eu-west-2"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"eu-west-3"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"sa-east-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,_s]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"us-east-2"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"us-west-1"]}],endpoint:R,[c]:f},{conditions:[{[l]:A,[m]:[S,"us-west-2"]}],endpoint:R,[c]:f},{endpoint:{url:bs,properties:{authSchemes:[{name:vs,signingName:ps,signingRegion:"{Region}"}]},headers:C},[c]:f}],[c]:b},{conditions:Gs,rules:[{conditions:Us,error:"Invalid Configuration: FIPS and custom endpoint are not supported",[c]:X},{conditions:Os,error:"Invalid Configuration: Dualstack and custom endpoint are not supported",[c]:X},{endpoint:{url:Ts,properties:C,headers:C},[c]:f}],[c]:b},{conditions:[ws],rules:[{conditions:[Ds],rules:[{conditions:[ks,Ks],rules:[{conditions:[{[l]:U,[m]:[qe,zs]},Ls],rules:[{endpoint:{url:"https://sts-fips.{Region}.{PartitionResult#dualStackDnsSuffix}",properties:C,headers:C},[c]:f}],[c]:b},{error:"FIPS and DualStack are enabled, but this partition does not support one or both",[c]:X}],[c]:b},{conditions:Us,rules:[{conditions:[{[l]:U,[m]:[zs,qe]}],rules:[{conditions:[{[l]:A,[m]:[{[l]:Je,[m]:[Fs,"name"]},"aws-us-gov"]}],endpoint:{url:"https://sts.{Region}.amazonaws.com",properties:C,headers:C},[c]:f},{endpoint:{url:"https://sts-fips.{Region}.{PartitionResult#dnsSuffix}",properties:C,headers:C},[c]:f}],[c]:b},{error:"FIPS is enabled but this partition does not support FIPS",[c]:X}],[c]:b},{conditions:Os,rules:[{conditions:[Ls],rules:[{endpoint:{url:"https://sts.{Region}.{PartitionResult#dualStackDnsSuffix}",properties:C,headers:C},[c]:f}],[c]:b},{error:"DualStack is enabled but this partition does not support DualStack",[c]:X}],[c]:b},Ms,{endpoint:{url:bs,properties:C,headers:C},[c]:f}],[c]:b}],[c]:b},{error:"Invalid Configuration: Missing Region",[c]:X}]},Sn=new Qe.kS({size:50,params:["Endpoint","Region","UseDualStack","UseFIPS","UseGlobalEndpoint"]}),Rn=(e,t={})=>Sn.get(e,()=>(0,Qe.sO)(An,{endpointParams:e,logger:t.logger}));Qe.mw.aws=gn.UF;const En=e=>({apiVersion:"2011-06-15",base64Decoder:e?.base64Decoder??Es.E,base64Encoder:e?.base64Encoder??Es.n,disableHostPrefix:e?.disableHostPrefix??!1,endpointProvider:e?.endpointProvider??Rn,extensions:e?.extensions??[],httpAuthSchemeProvider:e?.httpAuthSchemeProvider??cn,httpAuthSchemes:e?.httpAuthSchemes??[{schemeId:"aws.auth#sigv4",identityProvider:t=>t.getIdentityProvider("aws.auth#sigv4"),signer:new gs.f2},{schemeId:"smithy.api#noAuth",identityProvider:t=>t.getIdentityProvider("smithy.api#noAuth")||(async()=>({})),signer:new se.mR}],logger:e?.logger??new r.N4,serviceId:e?.serviceId??"STS",urlParser:e?.urlParser??yn.D,utf8Decoder:e?.utf8Decoder??Is.ar,utf8Encoder:e?.utf8Encoder??Is.Pq});var In=d(12165);const Cn=e=>{(0,r.I9)(process.version);const t=(0,In.I)(e),s=()=>t().then(r.lT),n=En(e);return(0,mn.I)(process.version),{...n,...e,runtime:"node",defaultsMode:t,bodyLengthChecker:e?.bodyLengthChecker??fn.n,credentialDefaultProvider:e?.credentialDefaultProvider??As.v6,defaultUserAgentProvider:e?.defaultUserAgentProvider??(0,Ss.pf)({serviceId:n.serviceId,clientVersion:ln.rE}),httpAuthSchemes:e?.httpAuthSchemes??[{schemeId:"aws.auth#sigv4",identityProvider:o=>o.getIdentityProvider("aws.auth#sigv4")||(async a=>await(0,As.v6)(a?.__config||{})()),signer:new gs.f2},{schemeId:"smithy.api#noAuth",identityProvider:o=>o.getIdentityProvider("smithy.api#noAuth")||(async()=>({})),signer:new se.mR}],maxAttempts:e?.maxAttempts??(0,Y.Z)(oe.qs),region:e?.region??(0,Y.Z)(ee.GG,ee.zH),requestHandler:Rs.$c.create(e?.requestHandler??s),retryMode:e?.retryMode??(0,Y.Z)({...oe.kN,default:async()=>(await s()).retryMode||hn.L0}),sha256:e?.sha256??un.V.bind(null,"sha256"),streamCollector:e?.streamCollector??Rs.kv,useDualstackEndpoint:e?.useDualstackEndpoint??(0,Y.Z)(ee.e$),useFipsEndpoint:e?.useFipsEndpoint??(0,Y.Z)(ee.Ko),userAgentAppId:e?.userAgentAppId??(0,Y.Z)(Ss.hV)}};var Hs=d(49402);const Pn=e=>{const t=e.httpAuthSchemes;let s=e.httpAuthSchemeProvider,n=e.credentials;return{setHttpAuthScheme(o){const a=t.findIndex(i=>i.schemeId===o.schemeId);a===-1?t.push(o):t.splice(a,1,o)},httpAuthSchemes(){return t},setHttpAuthSchemeProvider(o){s=o},httpAuthSchemeProvider(){return s},setCredentials(o){n=o},credentials(){return n}}},vn=e=>({httpAuthSchemes:e.httpAuthSchemes(),httpAuthSchemeProvider:e.httpAuthSchemeProvider(),credentials:e.credentials()}),re=e=>e,pn=(e,t)=>{const s={...re((0,Hs.Rq)(e)),...re((0,r.xA)(e)),...re((0,Se.eS)(e)),...re(Pn(e))};return t.forEach(n=>n.configure(s)),{...e,...(0,Hs.$3)(s),...(0,r.uv)(s),...(0,Se.jt)(s),...vn(s)}};class Xe extends r.Kj{constructor(...[t]){const s=Cn(t||{}),n=Zs(s),o=(0,fs.Dc)(n),a=(0,oe.$z)(o),i=(0,ee.TD)(a),I=(0,us.OV)(i),x=(0,ae.Co)(I),T=dn(x),O=pn(T,t?.extensions||[]);super(O),this.config=O,this.middlewareStack.use((0,fs.sM)(this.config)),this.middlewareStack.use((0,oe.ey)(this.config)),this.middlewareStack.use((0,tn.vK)(this.config)),this.middlewareStack.use((0,us.TC)(this.config)),this.middlewareStack.use((0,en.Y7)(this.config)),this.middlewareStack.use((0,sn.n4)(this.config)),this.middlewareStack.use((0,se.wB)(this.config,{httpAuthSchemeParametersProvider:on,identityProviderConfigProvider:async te=>new se.h$({"aws.auth#sigv4":te.credentials})})),this.middlewareStack.use((0,se.lW)(this.config))}destroy(){super.destroy()}}const js=(e,t)=>t?class extends e{constructor(n){super(n);for(const o of t)this.middlewareStack.use(o)}}:e,Ns=(e={},t)=>ds(e,js(Xe,t)),Bs=(e={},t)=>ls(e,js(Xe,t)),Jn=e=>t=>e({roleAssumer:Ns(t),roleAssumerWithWebIdentity:Bs(t),...t})}};
