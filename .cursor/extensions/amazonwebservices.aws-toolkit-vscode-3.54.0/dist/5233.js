"use strict";exports.id=5233,exports.ids=[5233],exports.modules={35233:(Qe,te,d)=>{d.d(te,{fromSSO:()=>Ye});var l=d(3631),W=d(70857),u=d(16928);const A={},oe=()=>process&&process.geteuid?`${process.geteuid()}`:"DEFAULT",D=()=>{const{HOME:e,USERPROFILE:s,HOMEPATH:t,HOMEDRIVE:o=`C:${u.sep}`}=process.env;if(e)return e;if(s)return s;if(t)return`${o}${t}`;const n=oe();return A[n]||(A[n]=(0,W.homedir)()),A[n]},ne="AWS_PROFILE",ie="default",re=e=>e.profile||process.env[ne]||ie;var U=d(76982);const ce=e=>{const t=(0,U.createHash)("sha1").update(e).digest("hex");return(0,u.join)(D(),".aws","sso","cache",`${t}.json`)};var E=d(79896);const{readFile:ae}=E.promises,le=async e=>{const s=ce(e),t=await ae(s,"utf8");return JSON.parse(t)};var p=d(31932);const fe=e=>Object.entries(e).filter(([s])=>{const t=s.indexOf(O);return t===-1?!1:Object.values(p.Ip).includes(s.substring(0,t))}).reduce((s,[t,o])=>{const n=t.indexOf(O),i=t.substring(0,n)===p.Ip.PROFILE?t.substring(n+1):t;return s[i]=o,s},{...e.default&&{default:e.default}}),de="AWS_CONFIG_FILE",G=()=>process.env[de]||(0,u.join)(D(),".aws","config"),ge="AWS_SHARED_CREDENTIALS_FILE",he=()=>process.env[ge]||(0,u.join)(D(),".aws","credentials"),ue=/^([\w-]+)\s(["'])?([\w-@\+\.%:/]+)\2$/,Se=["__proto__","profile __proto__"],R=e=>{const s={};let t,o;for(const n of e.split(/\r?\n/)){const i=n.split(/(^|\s)[;#]/)[0].trim();if(i[0]==="["&&i[i.length-1]==="]"){t=void 0,o=void 0;const c=i.substring(1,i.length-1),a=ue.exec(c);if(a){const[,r,,h]=a;Object.values(p.Ip).includes(r)&&(t=[r,h].join(O))}else t=c;if(Se.includes(c))throw new Error(`Found invalid profile name "${c}"`)}else if(t){const c=i.indexOf("=");if(![0,-1].includes(c)){const[a,r]=[i.substring(0,c).trim(),i.substring(c+1).trim()];if(r==="")o=a;else{o&&n.trimStart()===n&&(o=void 0),s[t]=s[t]||{};const h=o?[o,a].join(O):a;s[t][h]=r}}}}return s},{readFile:pe}=E.promises,v={},L=(e,s)=>((!v[e]||s?.ignoreCache)&&(v[e]=pe(e,"utf8")),v[e]),J=()=>({}),O=".",me=async(e={})=>{const{filepath:s=he(),configFilepath:t=G()}=e,o=D(),n="~/";let i=s;s.startsWith(n)&&(i=(0,u.join)(o,s.slice(2)));let f=t;t.startsWith(n)&&(f=(0,u.join)(o,t.slice(2)));const c=await Promise.all([L(f,{ignoreCache:e.ignoreCache}).then(R).then(fe).catch(J),L(i,{ignoreCache:e.ignoreCache}).then(R).catch(J)]);return{configFile:c[0],credentialsFile:c[1]}},we=e=>Object.entries(e).filter(([s])=>s.startsWith(p.Ip.SSO_SESSION+O)).reduce((s,[t,o])=>({...s,[t.substring(t.indexOf(O)+1)]:o}),{}),Fe=()=>({}),Oe=async(e={})=>L(e.configFilepath??G()).then(R).then(we).catch(Fe),Ce=(...e)=>{const s={};for(const t of e)for(const[o,n]of Object.entries(t))s[o]!==void 0?Object.assign(s[o],n):s[o]=n;return s},_e=async e=>{const s=await me(e);return Ce(s.configFile,s.credentialsFile)},Ee=e=>e&&(typeof e.sso_start_url=="string"||typeof e.sso_account_id=="string"||typeof e.sso_session=="string"||typeof e.sso_region=="string"||typeof e.sso_role_name=="string");var M=d(71500);const k={},Te=()=>process&&process.geteuid?`${process.geteuid()}`:"DEFAULT",N=()=>{const{HOME:e,USERPROFILE:s,HOMEPATH:t,HOMEDRIVE:o=`C:${u.sep}`}=process.env;if(e)return e;if(s)return s;if(t)return`${o}${t}`;const n=Te();return k[n]||(k[n]=(0,W.homedir)()),k[n]},Ie="AWS_PROFILE",xe="default",De=e=>e.profile||process.env[Ie]||xe,V=e=>{const t=(0,U.createHash)("sha1").update(e).digest("hex");return(0,u.join)(N(),".aws","sso","cache",`${t}.json`)},{readFile:Ne}=E.promises,ye=async e=>{const s=V(e),t=await Ne(s,"utf8");return JSON.parse(t)},Ae=e=>Object.entries(e).filter(([s])=>{const t=s.indexOf(C);return t===-1?!1:Object.values(p.Ip).includes(s.substring(0,t))}).reduce((s,[t,o])=>{const n=t.indexOf(C),i=t.substring(0,n)===p.Ip.PROFILE?t.substring(n+1):t;return s[i]=o,s},{...e.default&&{default:e.default}}),Re="AWS_CONFIG_FILE",X=()=>process.env[Re]||(0,u.join)(N(),".aws","config"),ve="AWS_SHARED_CREDENTIALS_FILE",Le=()=>process.env[ve]||(0,u.join)(N(),".aws","credentials"),ke=/^([\w-]+)\s(["'])?([\w-@\+\.%:/]+)\2$/,Pe=["__proto__","profile __proto__"],P=e=>{const s={};let t,o;for(const n of e.split(/\r?\n/)){const i=n.split(/(^|\s)[;#]/)[0].trim();if(i[0]==="["&&i[i.length-1]==="]"){t=void 0,o=void 0;const c=i.substring(1,i.length-1),a=ke.exec(c);if(a){const[,r,,h]=a;Object.values(p.Ip).includes(r)&&(t=[r,h].join(C))}else t=c;if(Pe.includes(c))throw new Error(`Found invalid profile name "${c}"`)}else if(t){const c=i.indexOf("=");if(![0,-1].includes(c)){const[a,r]=[i.substring(0,c).trim(),i.substring(c+1).trim()];if(r==="")o=a;else{o&&n.trimStart()===n&&(o=void 0),s[t]=s[t]||{};const h=o?[o,a].join(C):a;s[t][h]=r}}}}return s},{readFile:$e}=E.promises,$={},j=(e,s)=>((!$[e]||s?.ignoreCache)&&($[e]=$e(e,"utf8")),$[e]),B=()=>({}),C=".",je=async(e={})=>{const{filepath:s=Le(),configFilepath:t=X()}=e,o=N(),n="~/";let i=s;s.startsWith(n)&&(i=(0,u.join)(o,s.slice(2)));let f=t;t.startsWith(n)&&(f=(0,u.join)(o,t.slice(2)));const c=await Promise.all([j(f,{ignoreCache:e.ignoreCache}).then(P).then(Ae).catch(B),j(i,{ignoreCache:e.ignoreCache}).then(P).catch(B)]);return{configFile:c[0],credentialsFile:c[1]}},He=e=>Object.entries(e).filter(([s])=>s.startsWith(p.Ip.SSO_SESSION+C)).reduce((s,[t,o])=>({...s,[t.substring(t.indexOf(C)+1)]:o}),{}),be=()=>({}),Ke=async(e={})=>j(e.configFilepath??X()).then(P).then(He).catch(be),We=(...e)=>{const s={};for(const t of e)for(const[o,n]of Object.entries(t))s[o]!==void 0?Object.assign(s[o],n):s[o]=n;return s},Ue=async e=>{const s=await je(e);return We(s.configFile,s.credentialsFile)},Ge=5*60*1e3,H="To refresh this SSO session run 'aws sso login' with the corresponding profile.",b={},Je=async e=>{const{SSOOIDCClient:s}=await Promise.resolve().then(d.bind(d,57984));if(b[e])return b[e];const t=new s({region:e});return b[e]=t,t},Me=async(e,s)=>{const{CreateTokenCommand:t}=await Promise.resolve().then(d.bind(d,57984));return(await Je(s)).send(new t({clientId:e.clientId,clientSecret:e.clientSecret,refreshToken:e.refreshToken,grantType:"refresh_token"}))},z=e=>{if(e.expiration&&e.expiration.getTime()<Date.now())throw new l.Jh(`Token is expired. ${H}`,!1)},m=(e,s,t=!1)=>{if(typeof s>"u")throw new l.Jh(`Value not present for '${e}' in SSO Token${t?". Cannot refresh":""}. ${H}`,!1)},{writeFile:Ve}=E.promises,Xe=(e,s)=>{const t=V(e),o=JSON.stringify(s,null,2);return Ve(t,o)},Y=new Date(0),Be=(e={})=>async()=>{e.logger?.debug("@aws-sdk/token-providers - fromSso");const s=await Ue(e),t=De(e),o=s[t];if(o){if(!o.sso_session)throw new l.Jh(`Profile '${t}' is missing required property 'sso_session'.`)}else throw new l.Jh(`Profile '${t}' could not be found in shared credentials file.`,!1);const n=o.sso_session,f=(await Ke(e))[n];if(!f)throw new l.Jh(`Sso session '${n}' could not be found in shared credentials file.`,!1);for(const g of["sso_start_url","sso_region"])if(!f[g])throw new l.Jh(`Sso session '${n}' is missing required property '${g}'.`,!1);const c=f.sso_start_url,a=f.sso_region;let r;try{r=await ye(n)}catch{throw new l.Jh(`The SSO session token associated with profile=${t} was not found or is invalid. ${H}`,!1)}m("accessToken",r.accessToken),m("expiresAt",r.expiresAt);const{accessToken:h,expiresAt:I}=r,S={token:h,expiration:new Date(I)};if(S.expiration.getTime()-Date.now()>Ge)return S;if(Date.now()-Y.getTime()<30*1e3)return z(S),S;m("clientId",r.clientId,!0),m("clientSecret",r.clientSecret,!0),m("refreshToken",r.refreshToken,!0);try{Y.setTime(Date.now());const g=await Me(r,a);m("accessToken",g.accessToken),m("expiresIn",g.expiresIn);const _=new Date(Date.now()+g.expiresIn*1e3);try{await Xe(n,{...r,accessToken:g.accessToken,expiresAt:_.toISOString(),refreshToken:g.refreshToken})}catch{}return{token:g.accessToken,expiration:_}}catch{return z(S),S}},T=!1,Q=async({ssoStartUrl:e,ssoSession:s,ssoAccountId:t,ssoRegion:o,ssoRoleName:n,ssoClient:i,clientConfig:f,profile:c,logger:a})=>{let r;const h="To refresh this SSO session run aws sso login with the corresponding profile.";if(s)try{const F=await Be({profile:c})();r={accessToken:F.token,expiresAt:new Date(F.expiration).toISOString()}}catch(F){throw new l.C1(F.message,{tryNextLink:T,logger:a})}else try{r=await le(e)}catch{throw new l.C1(`The SSO session associated with this profile is invalid. ${h}`,{tryNextLink:T,logger:a})}if(new Date(r.expiresAt).getTime()-Date.now()<=0)throw new l.C1(`The SSO session associated with this profile has expired. ${h}`,{tryNextLink:T,logger:a});const{accessToken:I}=r,{SSOClient:S,GetRoleCredentialsCommand:g}=await d.e(42).then(d.bind(d,30042)),_=i||new S(Object.assign({},f??{},{region:f?.region??o}));let y;try{y=await _.send(new g({accountId:t,roleName:n,accessToken:I}))}catch(F){throw new l.C1(F,{tryNextLink:T,logger:a})}const{roleCredentials:{accessKeyId:w,secretAccessKey:x,sessionToken:Z,expiration:q,credentialScope:ee,accountId:se}={}}=y;if(!w||!x||!Z||!q)throw new l.C1("SSO returns an invalid temporary credential.",{tryNextLink:T,logger:a});const K={accessKeyId:w,secretAccessKey:x,sessionToken:Z,expiration:new Date(q),...ee&&{credentialScope:ee},...se&&{accountId:se}};return s?(0,M.g)(K,"CREDENTIALS_SSO","s"):(0,M.g)(K,"CREDENTIALS_SSO_LEGACY","u"),K},ze=(e,s)=>{const{sso_start_url:t,sso_account_id:o,sso_region:n,sso_role_name:i}=e;if(!t||!o||!n||!i)throw new l.C1(`Profile is configured with invalid SSO credentials. Required parameters "sso_account_id", "sso_region", "sso_role_name", "sso_start_url". Got ${Object.keys(e).join(", ")}
Reference: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html`,{tryNextLink:!1,logger:s});return e},Ye=(e={})=>async()=>{e.logger?.debug("@aws-sdk/credential-provider-sso - fromSSO");const{ssoStartUrl:s,ssoAccountId:t,ssoRegion:o,ssoRoleName:n,ssoSession:i}=e,{ssoClient:f}=e,c=re(e);if(!s&&!t&&!o&&!n&&!i){const r=(await _e(e))[c];if(!r)throw new l.C1(`Profile ${c} was not found.`,{logger:e.logger});if(!Ee(r))throw new l.C1(`Profile ${c} is not configured with SSO credentials.`,{logger:e.logger});if(r?.sso_session){const w=(await Oe(e))[r.sso_session],x=` configurations in profile ${c} and sso-session ${r.sso_session}`;if(o&&o!==w.sso_region)throw new l.C1("Conflicting SSO region"+x,{tryNextLink:!1,logger:e.logger});if(s&&s!==w.sso_start_url)throw new l.C1("Conflicting SSO start_url"+x,{tryNextLink:!1,logger:e.logger});r.sso_region=w.sso_region,r.sso_start_url=w.sso_start_url}const{sso_start_url:h,sso_account_id:I,sso_region:S,sso_role_name:g,sso_session:_}=ze(r,e.logger);return Q({ssoStartUrl:h,ssoSession:_,ssoAccountId:I,ssoRegion:S,ssoRoleName:g,ssoClient:f,clientConfig:e.clientConfig,profile:c})}else{if(!s||!t||!o||!n)throw new l.C1('Incomplete configuration. The fromSSO() argument hash must include "ssoStartUrl", "ssoAccountId", "ssoRegion", "ssoRoleName"',{tryNextLink:!1,logger:e.logger});return Q({ssoStartUrl:s,ssoSession:i,ssoAccountId:t,ssoRegion:o,ssoRoleName:n,ssoClient:f,clientConfig:e.clientConfig,profile:c})}}}};
