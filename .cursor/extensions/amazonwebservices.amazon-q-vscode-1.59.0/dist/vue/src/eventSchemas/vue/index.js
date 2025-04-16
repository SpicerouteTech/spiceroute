(()=>{"use strict";var y={7433:(s,e)=>{var i;i={value:!0},e.A=(o,a)=>{const r=o.__vccOpts||o;for(const[n,d]of a)r[n]=d;return r}}},v={};function w(s){var e=v[s];if(e!==void 0)return e.exports;var i=v[s]={exports:{}};return y[s](i,i.exports,w),i.exports}var m={};const t=Vue,E={id:"app"},V={class:"container button-container",style:{"justify-content":"space-between"}},D=["disabled"],k={id:"search_input"},C=["placeholder"],L={id:"result_content"},$={disabled:"",value:""},N=["value"],T={id:"schemaContent_versionDropdown"},P=["value"];function M(s,e,i,o,a,r){return(0,t.openBlock)(),(0,t.createElementBlock)("div",E,[(0,t.createElementVNode)("div",V,[(0,t.createElementVNode)("h1",null,(0,t.toDisplayString)(s.initialData.Header),1),(0,t.createElementVNode)("div",null,[(0,t.createElementVNode)("input",{type:"submit",disabled:s.downloadDisabled,onClick:e[0]||(e[0]=(...n)=>s.downloadClicked&&s.downloadClicked(...n)),value:"Download Code Bindings"},null,8,D)])]),(0,t.createElementVNode)("div",k,[(0,t.withDirectives)((0,t.createElementVNode)("input",{type:"search","onUpdate:modelValue":e[1]||(e[1]=n=>s.searchText=n),placeholder:s.initialData.SearchInputPlaceholder},null,8,C),[[t.vModelText,s.searchText]])]),(0,t.createElementVNode)("div",L,[(0,t.withDirectives)((0,t.createElementVNode)("select",{id:"searchList","onUpdate:modelValue":e[2]||(e[2]=n=>s.selectedSchema=n),onChange:e[3]||(e[3]=(...n)=>s.userSelectedSchema&&s.userSelectedSchema(...n)),size:"100"},[(0,t.createElementVNode)("option",$,(0,t.toDisplayString)(s.searchProgressInfo),1),((0,t.openBlock)(!0),(0,t.createElementBlock)(t.Fragment,null,(0,t.renderList)(s.searchResults,n=>((0,t.openBlock)(),(0,t.createElementBlock)("option",{key:n.RegistryName,value:n},(0,t.toDisplayString)(n.Title),9,N))),128))],544),[[t.vModelSelect,s.selectedSchema]]),(0,t.createElementVNode)("div",T,[(0,t.withDirectives)((0,t.createElementVNode)("select",{id:"versionList","onUpdate:modelValue":e[4]||(e[4]=n=>s.selectedVersion=n),onChange:e[5]||(e[5]=(...n)=>s.fetchSchemaContent&&s.fetchSchemaContent(...n))},[((0,t.openBlock)(!0),(0,t.createElementBlock)(t.Fragment,null,(0,t.renderList)(s.schemaVersions,n=>((0,t.openBlock)(),(0,t.createElementBlock)("option",{key:n,value:n},(0,t.toDisplayString)(s.initialData.VersionPrefix)+" "+(0,t.toDisplayString)(n),9,P))),128))],544),[[t.vModelSelect,s.selectedVersion]]),(0,t.withDirectives)((0,t.createElementVNode)("textarea",{readonly:"","onUpdate:modelValue":e[6]||(e[6]=n=>s.schemaContent=n)},null,512),[[t.vModelText,s.schemaContent]])])])])}class l{static registerGlobalCommands(){const e=new Event("remount");window.addEventListener("message",i=>{const{command:o}=i.data;if(o==="$clear"){vscode.setState({});for(const a of this.messageListeners)this.removeListener(a);window.dispatchEvent(e)}})}static addListener(e){this.messageListeners.add(e),window.addEventListener("message",e)}static removeListener(e){this.messageListeners.delete(e),window.removeEventListener("message",e)}static sendRequest(e,i,o){const a=JSON.parse(JSON.stringify(o)),r=new Promise((n,d)=>{const p=F=>{const c=F.data;if(e===c.id)if(this.removeListener(p),window.clearTimeout(R),c.error===!0){const A=JSON.parse(c.data);d(new Error(A.message))}else c.event?(typeof o[0]!="function"&&d(new Error(`Expected frontend event handler to be a function: ${i}`)),n(this.registerEventHandler(i,o[0]))):n(c.data)},R=setTimeout(()=>{this.removeListener(p),d(new Error(`Timed out while waiting for response: id: ${e}, command: ${i}`))},3e5);this.addListener(p)});return vscode.postMessage({id:e,command:i,data:a}),r}static registerEventHandler(e,i){const o=a=>{const r=a.data;if(r.command===e){if(!r.event)throw new Error(`Expected backend handler to be an event emitter: ${e}`);i(r.data)}};return this.addListener(o),{dispose:()=>this.removeListener(o)}}static create(){return this.initialized||(this.initialized=!0,this.registerGlobalCommands()),new Proxy({},{set:()=>{throw new TypeError("Cannot set property to webview client")},get:(e,i)=>{if(typeof i!="string"){console.warn(`Tried to index webview client with non-string property: ${String(i)}`);return}if(i==="init"){const a=vscode.getState()??{};if(a.__once)return()=>Promise.resolve();vscode.setState(Object.assign(a,{__once:!0}))}const o=(this.counter++).toString();return(...a)=>this.sendRequest(o,i,a)}})}}l.counter=0,l.initialized=!1,l.messageListeners=new Set;const h=new Set;window.addEventListener("remount",()=>h.clear());const O={created(){if(this.$data===void 0)return;const s=vscode.getState()??{};this.$options._count=(this.$options._count??0)+1;const e=this.id??`${this.name??`DEFAULT-${h.size}`}-${this.$options._count}`;if(this.$options._unid=e,h.has(e)){console.warn(`Component "${e}" already exists. State-saving functionality will be disabled.`);return}h.add(e);const i=s[e]??{};for(const o of Object.keys(this.$data))this.$data[o]=i[o]??this.$data[o];for(const o of Object.keys(this.$data))this.$watch(o,a=>{const r=vscode.getState()??{},n=Object.assign(r[e]??{},{[o]:a!==void 0?JSON.parse(JSON.stringify(a)):void 0});vscode.setState(Object.assign(r,{[e]:n}))},{deep:!0})}},u=l.create();let g;const x=(0,t.defineComponent)({data(){return{initialData:{Header:"",SearchInputPlaceholder:"",VersionPrefix:"",RegistryNames:[],Region:"",LocalizedMessages:{noSchemasFound:"",searching:"",loading:"",select:""}},searchText:"",searchProgressInfo:"",searchResults:[],selectedSchema:{},selectedVersion:"",schemaContent:"",schemaVersions:[],downloadDisabled:!0}},watch:{searchText:function(s,e){window.clearTimeout(g),g=window.setTimeout(()=>this.userSearchedText(),250)}},async created(){this.initialData=await u.init()??this.initialData},methods:{async userSearchedText(){if(this.resetSearchResults(),this.resetSchemaContentAndVersionDropdown(),this.downloadDisabled=!0,this.searchText===""){this.searchProgressInfo=this.initialData.LocalizedMessages.noSchemasFound;return}this.searchProgressInfo=this.initialData.LocalizedMessages.searching;const s=await u.searchSchemas(this.searchText);if(s.resultsNotFound){this.searchProgressInfo=this.initialData.LocalizedMessages.noSchemasFound;return}this.searchProgressInfo=this.initialData.LocalizedMessages.select,this.searchResults=s.results},userSelectedSchema:function(){this.resetSchemaContentAndVersionDropdown(),this.downloadDisabled=!1,this.fetchSchemaContent()},downloadClicked:function(){u.downloadCodeBindings(this.selectedSchema)},async fetchSchemaContent(){this.schemaContent=this.initialData.LocalizedMessages.loading;const s=await u.fetchSchemaContent(this.selectedSchema,this.selectedVersion);this.schemaContent=s.results,this.selectedVersion=s.version,this.schemaVersions=s.versionList??this.schemaVersions},resetSearchResults:function(){this.selectedSchema={},this.searchResults=[],this.searchProgressInfo=""},resetSchemaContentAndVersionDropdown:function(){this.selectedVersion="",this.schemaContent="",this.schemaVersions=[]}},mixins:[O]});var B=w(7433);const z=(0,B.A)(x,[["render",M]]);const f=()=>(0,t.createApp)(z),_=f();_.mount("#vue-app"),window.addEventListener("remount",()=>{_.unmount(),f().mount("#vue-app")});var S=this;for(var b in m)S[b]=m[b];m.__esModule&&Object.defineProperty(S,"__esModule",{value:!0})})();
/*!
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
