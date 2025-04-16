"use strict";exports.id=3432,exports.ids=[3432],exports.modules={53432:(ie,w,i)=>{i.d(w,{fromIni:()=>re});var x=i(70857),u=i(16928);const E={},T=()=>process&&process.geteuid?`${process.geteuid()}`:"DEFAULT",C=()=>{const{HOME:e,USERPROFILE:t,HOMEPATH:n,HOMEDRIVE:s=`C:${u.sep}`}=process.env;if(e)return e;if(t)return t;if(n)return`${s}${n}`;const r=T();return E[r]||(E[r]=(0,x.homedir)()),E[r]},N="AWS_PROFILE",j="default",I=e=>e.profile||process.env[N]||j;var ce=i(76982);const ae=e=>{const n=createHash("sha1").update(e).digest("hex");return join(getHomeDir(),".aws","sso","cache",`${n}.json`)};var O=i(79896);const{readFile:b}=O.promises,le=async e=>{const t=getSSOTokenFilepath(e),n=await b(t,"utf8");return JSON.parse(n)};var m=i(31932);const $=e=>Object.entries(e).filter(([t])=>{const n=t.indexOf(h);return n===-1?!1:Object.values(m.Ip).includes(t.substring(0,n))}).reduce((t,[n,s])=>{const r=n.indexOf(h),o=n.substring(0,r)===m.Ip.PROFILE?n.substring(r+1):n;return t[o]=s,t},{...e.default&&{default:e.default}}),W="AWS_CONFIG_FILE",H=()=>process.env[W]||(0,u.join)(C(),".aws","config"),_="AWS_SHARED_CREDENTIALS_FILE",M=()=>process.env[_]||(0,u.join)(C(),".aws","credentials"),K=/^([\w-]+)\s(["'])?([\w-@\+\.%:/]+)\2$/,G=["__proto__","profile __proto__"],P=e=>{const t={};let n,s;for(const r of e.split(/\r?\n/)){const o=r.split(/(^|\s)[;#]/)[0].trim();if(o[0]==="["&&o[o.length-1]==="]"){n=void 0,s=void 0;const c=o.substring(1,o.length-1),a=K.exec(c);if(a){const[,f,,S]=a;Object.values(m.Ip).includes(f)&&(n=[f,S].join(h))}else n=c;if(G.includes(c))throw new Error(`Found invalid profile name "${c}"`)}else if(n){const c=o.indexOf("=");if(![0,-1].includes(c)){const[a,f]=[o.substring(0,c).trim(),o.substring(c+1).trim()];if(f==="")s=a;else{s&&r.trimStart()===r&&(s=void 0),t[n]=t[n]||{};const S=s?[s,a].join(h):a;t[n][S]=f}}}}return t},{readFile:B}=O.promises,y={},v=(e,t)=>((!y[e]||t?.ignoreCache)&&(y[e]=B(e,"utf8")),y[e]),R=()=>({}),h=".",U=async(e={})=>{const{filepath:t=M(),configFilepath:n=H()}=e,s=C(),r="~/";let o=t;t.startsWith(r)&&(o=(0,u.join)(s,t.slice(2)));let d=n;n.startsWith(r)&&(d=(0,u.join)(s,n.slice(2)));const c=await Promise.all([v(d,{ignoreCache:e.ignoreCache}).then(P).then($).catch(R),v(o,{ignoreCache:e.ignoreCache}).then(P).catch(R)]);return{configFile:c[0],credentialsFile:c[1]}},de=e=>Object.entries(e).filter(([t])=>t.startsWith(IniSectionType.SSO_SESSION+CONFIG_PREFIX_SEPARATOR)).reduce((t,[n,s])=>({...t,[n.substring(n.indexOf(CONFIG_PREFIX_SEPARATOR)+1)]:s}),{}),V=()=>({}),fe=async(e={})=>slurpFile(e.configFilepath??getConfigFilepath()).then(parseIni).then(getSsoSessionData).catch(V),X=(...e)=>{const t={};for(const n of e)for(const[s,r]of Object.entries(n))t[s]!==void 0?Object.assign(t[s],r):t[s]=r;return t},k=async e=>{const t=await U(e);return X(t.configFile,t.credentialsFile)};var g=i(3631),l=i(71500);const J=(e,t,n)=>{const s={EcsContainer:async r=>{const{fromHttp:o}=await i.e(7251).then(i.bind(i,87251)),{fromContainerMetadata:d}=await Promise.resolve().then(i.bind(i,40728));return n?.debug("@aws-sdk/credential-provider-ini - credential_source is EcsContainer"),async()=>(0,g.cy)(o(r??{}),d(r))().then(F)},Ec2InstanceMetadata:async r=>{n?.debug("@aws-sdk/credential-provider-ini - credential_source is Ec2InstanceMetadata");const{fromInstanceMetadata:o}=await Promise.resolve().then(i.bind(i,40728));return async()=>o(r)().then(F)},Environment:async r=>{n?.debug("@aws-sdk/credential-provider-ini - credential_source is Environment");const{fromEnv:o}=await Promise.resolve().then(i.bind(i,97215));return async()=>o(r)().then(F)}};if(e in s)return s[e];throw new g.C1(`Unsupported credential source in profile ${t}. Got ${e}, expected EcsContainer or Ec2InstanceMetadata or Environment.`,{logger:n})},F=e=>(0,l.g)(e,"CREDENTIALS_PROFILE_NAMED_PROVIDER","p"),Y=(e,{profile:t="default",logger:n}={})=>Boolean(e)&&typeof e=="object"&&typeof e.role_arn=="string"&&["undefined","string"].indexOf(typeof e.role_session_name)>-1&&["undefined","string"].indexOf(typeof e.external_id)>-1&&["undefined","string"].indexOf(typeof e.mfa_serial)>-1&&(z(e,{profile:t,logger:n})||Q(e,{profile:t,logger:n})),z=(e,{profile:t,logger:n})=>{const s=typeof e.source_profile=="string"&&typeof e.credential_source>"u";return s&&n?.debug?.(`    ${t} isAssumeRoleWithSourceProfile source_profile=${e.source_profile}`),s},Q=(e,{profile:t,logger:n})=>{const s=typeof e.credential_source=="string"&&typeof e.source_profile>"u";return s&&n?.debug?.(`    ${t} isCredentialSourceProfile credential_source=${e.credential_source}`),s},Z=async(e,t,n,s={})=>{n.logger?.debug("@aws-sdk/credential-provider-ini - resolveAssumeRoleCredentials (STS)");const r=t[e];if(!n.roleAssumer){const{getDefaultRoleAssumer:c}=await i.e(8328).then(i.bind(i,18328));n.roleAssumer=c({...n.clientConfig,credentialProviderLogger:n.logger,parentClientConfig:n?.parentClientConfig},n.clientPlugins)}const{source_profile:o}=r;if(o&&o in s)throw new g.C1(`Detected a cycle attempting to resolve credentials for profile ${I(n)}. Profiles visited: `+Object.keys(s).join(", "),{logger:n.logger});n.logger?.debug(`@aws-sdk/credential-provider-ini - finding credential resolver using ${o?`source_profile=[${o}]`:`profile=[${e}]`}`);const d=o?L(o,t,n,{...s,[o]:!0},p(t[o]??{})):(await J(r.credential_source,e,n.logger)(n))();if(p(r))return d.then(c=>(0,l.g)(c,"CREDENTIALS_PROFILE_SOURCE_PROFILE","o"));{const c={RoleArn:r.role_arn,RoleSessionName:r.role_session_name||`aws-sdk-js-${Date.now()}`,ExternalId:r.external_id,DurationSeconds:parseInt(r.duration_seconds||"3600",10)},{mfa_serial:a}=r;if(a){if(!n.mfaCodeProvider)throw new g.C1(`Profile ${e} requires multi-factor authentication, but no MFA code callback was provided.`,{logger:n.logger,tryNextLink:!1});c.SerialNumber=a,c.TokenCode=await n.mfaCodeProvider(a)}const f=await d;return n.roleAssumer(f,c).then(S=>(0,l.g)(S,"CREDENTIALS_PROFILE_SOURCE_PROFILE","o"))}},p=e=>!e.role_arn&&!!e.credential_source,q=e=>Boolean(e)&&typeof e=="object"&&typeof e.credential_process=="string",ee=async(e,t)=>Promise.resolve().then(i.bind(i,27084)).then(({fromProcess:n})=>n({...e,profile:t})().then(s=>(0,l.g)(s,"CREDENTIALS_PROFILE_PROCESS","v"))),ne=async(e,t,n={})=>{const{fromSSO:s}=await i.e(5233).then(i.bind(i,35233));return s({profile:e,logger:n.logger})().then(r=>t.sso_session?(0,l.g)(r,"CREDENTIALS_PROFILE_SSO","r"):(0,l.g)(r,"CREDENTIALS_PROFILE_SSO_LEGACY","t"))},te=e=>e&&(typeof e.sso_start_url=="string"||typeof e.sso_account_id=="string"||typeof e.sso_session=="string"||typeof e.sso_region=="string"||typeof e.sso_role_name=="string"),A=e=>Boolean(e)&&typeof e=="object"&&typeof e.aws_access_key_id=="string"&&typeof e.aws_secret_access_key=="string"&&["undefined","string"].indexOf(typeof e.aws_session_token)>-1&&["undefined","string"].indexOf(typeof e.aws_account_id)>-1,D=async(e,t)=>{t?.logger?.debug("@aws-sdk/credential-provider-ini - resolveStaticCredentials");const n={accessKeyId:e.aws_access_key_id,secretAccessKey:e.aws_secret_access_key,sessionToken:e.aws_session_token,...e.aws_credential_scope&&{credentialScope:e.aws_credential_scope},...e.aws_account_id&&{accountId:e.aws_account_id}};return(0,l.g)(n,"CREDENTIALS_PROFILE","n")},se=e=>Boolean(e)&&typeof e=="object"&&typeof e.web_identity_token_file=="string"&&typeof e.role_arn=="string"&&["undefined","string"].indexOf(typeof e.role_session_name)>-1,oe=async(e,t)=>i.e(9155).then(i.bind(i,39155)).then(({fromTokenFile:n})=>n({webIdentityTokenFile:e.web_identity_token_file,roleArn:e.role_arn,roleSessionName:e.role_session_name,roleAssumerWithWebIdentity:t.roleAssumerWithWebIdentity,logger:t.logger,parentClientConfig:t.parentClientConfig})().then(s=>(0,l.g)(s,"CREDENTIALS_PROFILE_STS_WEB_ID_TOKEN","q"))),L=async(e,t,n,s={},r=!1)=>{const o=t[e];if(Object.keys(s).length>0&&A(o))return D(o,n);if(r||Y(o,{profile:e,logger:n.logger}))return Z(e,t,n,s);if(A(o))return D(o,n);if(se(o))return oe(o,n);if(q(o))return ee(n,e);if(te(o))return await ne(e,o,n);throw new g.C1(`Could not resolve credentials using profile: [${e}] in configuration/credentials file(s).`,{logger:n.logger})},re=(e={})=>async()=>{e.logger?.debug("@aws-sdk/credential-provider-ini - fromIni");const t=await k(e);return L(I(e),t,e)}}};
