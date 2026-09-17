/* ============================================================
   Tiffin — nutrition tracker
   Vanilla JS, single-file app. FOOD_DB is defined in a script
   tag loaded before this one.
   ============================================================ */
(function(){
"use strict";

/* ---------- Icons ---------- */
const ICON = {
  home:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11.5 12 4l8 7.5"/><path d="M6 10v9a1 1 0 0 0 1 1h3v-5h4v5h3a1 1 0 0 0 1-1v-9"/></svg>',
  foods:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M20 20l-4.8-4.8"/></svg>',
  scan:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16"/><path d="M7 9v6M10 9v6M13 9v6M16 9v6"/></svg>',
  progress:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V9M10 19V5M16 19v-7M22 19H2"/></svg>',
  nutrients:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><path d="M12 4v8l6 4"/></svg>',
  profile:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8.5" r="3.5"/><path d="M4.5 20c1.2-4 4-6 7.5-6s6.3 2 7.5 6"/></svg>',
  flame:'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2c1 3-3 4.5-3 8a4 4 0 0 0 8 0c0-1.3-.5-2-1-2.7.7 3-1 4.7-2.6 4.7C11.6 12 11 10.7 11 9c0-2.5 2-4 1-7Zm-5.4 9.7C5.6 13 5 14.6 5 16.2 5 19.4 8.1 22 12 22s7-2.6 7-5.8c0-2.6-1.3-4.4-2.5-5.7.2 3.6-2 6-4.5 6-2.7 0-4.3-2-4-4.6-.7.7-1.3 1.6-1.4 1.8Z"/></svg>',
  plus:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
  x:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  chevLeft:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>',
  chevRight:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>',
  chevUp:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 15l6-6 6 6"/></svg>',
  chevDown:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>',
  pencil:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 16.5V20h3.5L18.5 9 15 5.5 4 16.5Z"/><path d="M13.5 7 17 10.5"/></svg>',
  camera:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1Z"/><circle cx="12" cy="13" r="3.3"/></svg>',
  check:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7"/></svg>',
};

/* ---------- Constants ---------- */
const STORAGE_KEY = 'tiffin_state_v1';
const EMOJI_PALETTE = ['🍳','🍚','🍽️','🍎','🍪','🥗','🍜','☕','🥪','🍲','🌮','🍱','🥞','🍇'];

const NUTRIENT_KEYS = [
  'kcal','protein','carbs','fat','satFat','fiber','sugar','sodium','potassium','calcium','iron','vitA','vitC',
  'addedSugar','mufa','pufa','omega3Ala','omega3Epa','omega3Dha','omega6La',
  'vitD','vitE','vitK','vitB1','vitB2','vitB3','vitB5','vitB6','vitB7','vitB9','vitB12',
  'magnesium','phosphorus','chloride','zinc','copper','manganese','selenium','iodine','chromium','molybdenum',
  'choline','caffeine','solubleFiber','creatine'
];

const NUTRIENT_GROUPS = [
  {title:'Macros', rows:[
    ['protein','Protein','g','proteinGoal'],
    ['carbs','Carbohydrates','g','carbGoal'],
    ['fat','Fat','g','fatGoal'],
    ['fiber','Fiber','g','fiberGoal'],
    ['sugar','Total Sugar','g',null],
    ['addedSugar','Added Sugar','g','addedSugarLimit',true],
  ]},
  {title:'Fats detail', rows:[
    ['satFat','Saturated Fat','g',null],
    ['mufa','MUFA','g',null],
    ['pufa','PUFA','g',null],
    ['omega3Ala','Omega-3 (ALA)','g','omega3AlaGoal'],
    ['omega3Epa','EPA','g',null],
    ['omega3Dha','DHA','g',null],
    ['omega6La','Omega-6 (LA)','g',null],
  ]},
  {title:'Vitamins', rows:[
    ['vitA','Vitamin A','mcg','vitAGoal'],
    ['vitB1','B1 (Thiamine)','mg','vitB1Goal'],
    ['vitB2','B2 (Riboflavin)','mg','vitB2Goal'],
    ['vitB3','B3 (Niacin)','mg','vitB3Goal'],
    ['vitB5','B5 (Pantothenic Acid)','mg','vitB5Goal'],
    ['vitB6','B6','mg','vitB6Goal'],
    ['vitB7','B7 (Biotin)','mcg','vitB7Goal'],
    ['vitB9','B9 (Folate)','mcg','vitB9Goal'],
    ['vitB12','B12','mcg','vitB12Goal'],
    ['vitC','Vitamin C','mg','vitCGoal'],
    ['vitD','Vitamin D','mcg','vitDGoal'],
    ['vitE','Vitamin E','mg','vitEGoal'],
    ['vitK','Vitamin K','mcg','vitKGoal'],
  ]},
  {title:'Minerals', rows:[
    ['calcium','Calcium','mg','calciumGoal'],
    ['magnesium','Magnesium','mg','magnesiumGoal'],
    ['phosphorus','Phosphorus','mg','phosphorusGoal'],
    ['potassium','Potassium','mg','potassiumGoal'],
    ['sodium','Sodium','mg','sodiumLimit',true],
    ['chloride','Chloride','mg','chlorideGoal'],
    ['iron','Iron','mg','ironGoal'],
    ['zinc','Zinc','mg','zincGoal'],
    ['copper','Copper','mg','copperGoal'],
    ['manganese','Manganese','mg','manganeseGoal'],
    ['selenium','Selenium','mcg','seleniumGoal'],
    ['iodine','Iodine','mcg','iodineGoal'],
    ['chromium','Chromium','mcg','chromiumGoal'],
    ['molybdenum','Molybdenum','mcg','molybdenumGoal'],
  ]},
  {title:'Other', rows:[
    ['choline','Choline','mg','cholineGoal'],
    ['caffeine','Caffeine','mg','caffeineLimit',true],
    ['solubleFiber','Soluble Fiber','g',null],
    ['creatine','Creatine','mg',null],
  ]},
];

const FIXED_TARGETS = {
  addedSugarLimit:50, omega3AlaGoal:1.4,
  vitB1Goal:1.2, vitB2Goal:1.3, vitB3Goal:16, vitB5Goal:5, vitB6Goal:1.7, vitB7Goal:30, vitB9Goal:400, vitB12Goal:2.4,
  vitDGoal:15, vitEGoal:15, vitKGoal:90,
  magnesiumGoal:400, phosphorusGoal:700, chlorideGoal:2300, zincGoal:11, copperGoal:0.9, manganeseGoal:2.3,
  seleniumGoal:55, iodineGoal:150, chromiumGoal:35, molybdenumGoal:45,
  cholineGoal:550, caffeineLimit:400,
};

const ACTIVITY_MULT = {sedentary:1.2, light:1.375, moderate:1.55, active:1.725, very_active:1.9};
const ACTIVITY_LABEL = {sedentary:'Sedentary (little exercise)', light:'Light (1-3 days/wk)', moderate:'Moderate (3-5 days/wk)', active:'Active (6-7 days/wk)', very_active:'Very active (2x/day or physical job)'};

const DEFAULT_GOALS = {
  calorieGoal:2000, proteinGoal:100, carbGoal:250, fatGoal:65, fiberGoal:30,
  sodiumLimit:2300, potassiumGoal:3500, calciumGoal:1000, ironGoal:18, vitAGoal:900, vitCGoal:90,
  weightGoalKg:null, startWeightKg:null, unit:'metric', theme:'system', waterGoalMl:2500,
};

function defaultMealSlots(){
  return [
    {id:'meal-1', name:'Meal 1', emoji:'🍳'},
    {id:'meal-2', name:'Meal 2', emoji:'🍚'},
    {id:'meal-3', name:'Meal 3', emoji:'🍽️'},
    {id:'meal-4', name:'Meal 4', emoji:'🍎'},
    {id:'meal-5', name:'Meal 5', emoji:'🍪'},
  ];
}
function defaultProfile(){
  return { name:'', sex:null, age:null, heightCm:null, heightUnit:'cm', activityLevel:'moderate', goalType:'maintain', weeklyRateKg:0 };
}
function defaultState(){
  return {
    goals:{...DEFAULT_GOALS}, profile:defaultProfile(), diary:{}, weightLog:[],
    customFoods:[], customMeals:[], barcodeMap:{}, mealSlots: defaultMealSlots(),
  };
}

/* ---------- Storage ---------- */
let storageOk = true;
// Copies only keys already present on `defaults` from `source`, so a
// stored/imported JSON blob can never introduce arbitrary keys (including
// "__proto__", which Object.assign(target, source) would otherwise use to
// repoint target's prototype — CWE-1321 prototype pollution).
function mergeKnownFields(defaults, source){
  const out = Object.assign({}, defaults);
  if(source && typeof source === 'object'){
    Object.keys(defaults).forEach(k=>{
      if(Object.prototype.hasOwnProperty.call(source, k)) out[k] = source[k];
    });
  }
  return out;
}
function loadState(){
  try{
    const raw = localStorage.getItem(STORAGE_KEY);
    if(!raw) return defaultState();
    const parsed = JSON.parse(raw);
    const s = defaultState();
    s.goals = mergeKnownFields(DEFAULT_GOALS, parsed.goals);
    s.profile = mergeKnownFields(defaultProfile(), parsed.profile);
    s.diary = parsed.diary || {};
    s.weightLog = Array.isArray(parsed.weightLog) ? parsed.weightLog : [];
    s.customFoods = Array.isArray(parsed.customFoods) ? parsed.customFoods : [];
    s.customMeals = Array.isArray(parsed.customMeals) ? parsed.customMeals : [];
    s.barcodeMap = parsed.barcodeMap || {};
    if(Array.isArray(parsed.mealSlots) && parsed.mealSlots.length){
      s.mealSlots = parsed.mealSlots;
    } else {
      s.mealSlots = defaultMealSlots();
      const legacy = {breakfast:'meal-1', lunch:'meal-2', dinner:'meal-3', snacks:'meal-4'};
      Object.keys(s.diary).forEach(dateKey=>{
        const day = s.diary[dateKey] || {};
        const newDay = {};
        Object.keys(day).forEach(k=>{
          const nk = legacy[k] || k;
          if(Array.isArray(day[k])) newDay[nk] = (newDay[nk]||[]).concat(day[k]);
          else newDay[k] = day[k];
        });
        s.diary[dateKey] = newDay;
      });
    }
    return s;
  }catch(e){
    storageOk = false;
    return defaultState();
  }
}
function saveState(){
  try{ localStorage.setItem(STORAGE_KEY, JSON.stringify(STATE)); }
  catch(e){ storageOk = false; }
}

let STATE = loadState();

/* ---------- Utilities ---------- */
function uid(){ return Math.random().toString(36).slice(2,9); }
function round1(n){ return Math.round((n + Number.EPSILON) * 10) / 10; }
function clamp(v,a,b){ return Math.max(a, Math.min(b, v)); }
function pad2(n){ return n < 10 ? '0'+n : ''+n; }
function toKey(d){ return d.getFullYear()+'-'+pad2(d.getMonth()+1)+'-'+pad2(d.getDate()); }
function todayKey(){ return toKey(new Date()); }
function keyToDate(key){ const [y,m,d] = key.split('-').map(Number); return new Date(y, m-1, d); }
function addDaysKey(key, delta){ const d = keyToDate(key); d.setDate(d.getDate()+delta); return toKey(d); }
function fmtDateLabel(key){
  const t = todayKey();
  if(key === t) return 'Today';
  if(key === addDaysKey(t,-1)) return 'Yesterday';
  if(key === addDaysKey(t,1)) return 'Tomorrow';
  const d = keyToDate(key);
  return d.toLocaleDateString(undefined, {weekday:'short', day:'numeric', month:'short'});
}
function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function css(varName){ return getComputedStyle(document.documentElement).getPropertyValue(varName).trim(); }

/* ---------- Meal slots ---------- */
function mealSlot(id){ return STATE.mealSlots.find(s=>s.id===id) || null; }
function mealName(id){ const s = mealSlot(id); return s ? s.name : 'Meal'; }
function mealEmoji(id){ const s = mealSlot(id); return s ? s.emoji : '🍽️'; }

/* ---------- Food resolution ---------- */
function dbFoodById(id){ return FOOD_DB.find(f=>f.id===id) || null; }
function customFoodById(id){ return STATE.customFoods.find(f=>f.id===id) || null; }
function mealDefById(id){ return STATE.customMeals.find(m=>m.id===id) || null; }
function zeroNutrients(){ const o = {}; NUTRIENT_KEYS.forEach(k=>o[k]=0); return o; }
function scaleNutrients(base, qty){ const o = {}; NUTRIENT_KEYS.forEach(k=> o[k] = (base[k]||0) * qty); return o; }
function addNutrients(a,b){ const o = {}; NUTRIENT_KEYS.forEach(k=> o[k] = (a[k]||0) + (b[k]||0)); return o; }

function resolveRefBase(ref){
  if(!ref) return null;
  if(ref.type === 'db'){
    const f = dbFoodById(ref.id); if(!f) return null;
    return {name:f.name, servingLabel:f.servingLabel, servingGrams:f.servingGrams, nutrients:f, kind:'db', category:f.category};
  }
  if(ref.type === 'custom'){
    const f = customFoodById(ref.id); if(!f) return null;
    return {name:f.name, servingLabel:f.servingLabel, servingGrams:f.servingGrams, nutrients:f, kind:'custom', category:'Custom'};
  }
  if(ref.type === 'meal'){
    const m = mealDefById(ref.id); if(!m) return null;
    let n = zeroNutrients(); let grams = 0;
    m.items.forEach(it=>{
      const b = resolveRefBase(it.ref);
      if(!b) return;
      n = addNutrients(n, scaleNutrients(b.nutrients, it.qty));
      grams += (b.servingGrams||0) * it.qty;
    });
    return {name:m.name, servingLabel:'1 recipe', servingGrams:grams, nutrients:n, kind:'meal', category:'Meal'};
  }
  return null;
}
function entryNutrients(entry){
  const base = resolveRefBase(entry.ref);
  if(!base) return zeroNutrients();
  return scaleNutrients(base.nutrients, entry.qty);
}

/* ---------- Diary ---------- */
function getDay(key){
  if(!STATE.diary[key]) STATE.diary[key] = {};
  const d = STATE.diary[key];
  STATE.mealSlots.forEach(s=>{ if(!d[s.id]) d[s.id] = []; });
  if(typeof d.water !== 'number') d.water = 0;
  if(!Array.isArray(d.workouts)) d.workouts = [];
  return d;
}
function refsEqual(a,b){ return !!a && !!b && a.type===b.type && a.id===b.id; }
function purgeFoodRef(ref){
  Object.keys(STATE.diary).forEach(dateKey=>{
    const day = STATE.diary[dateKey];
    STATE.mealSlots.forEach(slot=>{
      if(Array.isArray(day[slot.id])) day[slot.id] = day[slot.id].filter(entry=> !refsEqual(entry.ref, ref));
    });
  });
  STATE.customMeals.forEach(m=>{ m.items = m.items.filter(it=> !refsEqual(it.ref, ref)); });
}
function dayHasEntries(key){
  const d = STATE.diary[key];
  if(!d) return false;
  return STATE.mealSlots.some(s => Array.isArray(d[s.id]) && d[s.id].length > 0);
}
function dayTotals(key){
  const d = getDay(key);
  let total = zeroNutrients();
  STATE.mealSlots.forEach(s=>{ (d[s.id]||[]).forEach(entry=>{ total = addNutrients(total, entryNutrients(entry)); }); });
  return total;
}
function mealTotal(key, mealId){
  const d = getDay(key);
  let t = zeroNutrients();
  (d[mealId]||[]).forEach(e=> t = addNutrients(t, entryNutrients(e)));
  return t;
}
function computeStreak(){
  let d = todayKey();
  if(!dayHasEntries(d)) d = addDaysKey(d,-1);
  let count = 0;
  while(dayHasEntries(d)){ count++; d = addDaysKey(d,-1); }
  return count;
}

/* ---------- Weight / units ---------- */
function kgToLb(kg){ return kg / 0.45359237; }
function lbToKg(lb){ return lb * 0.45359237; }
function toDisplayWeight(kg){ return STATE.goals.unit === 'imperial' ? kgToLb(kg) : kg; }
function fromDisplayWeight(v){ return STATE.goals.unit === 'imperial' ? lbToKg(v) : v; }
function weightUnitLabel(){ return STATE.goals.unit === 'imperial' ? 'lb' : 'kg'; }
function latestWeightKg(){
  if(STATE.weightLog.length){
    const sorted = [...STATE.weightLog].sort((a,b)=> a.date < b.date ? -1 : 1);
    return sorted[sorted.length-1].kg;
  }
  return STATE.goals.startWeightKg;
}

/* ---------- Energy calculations ---------- */
function calcBMR(){
  const p = STATE.profile;
  if(!p.sex || !p.age || !p.heightCm) return null;
  const weight = latestWeightKg();
  if(weight == null) return null;
  const s = p.sex === 'male' ? 5 : -161;
  return 10*weight + 6.25*p.heightCm - 5*p.age + s;
}
function calcTDEE(){
  const bmr = calcBMR(); if(bmr == null) return null;
  const mult = ACTIVITY_MULT[STATE.profile.activityLevel || 'moderate'];
  return bmr * mult;
}
function calculateTargetsFromProfile(){
  const bmr = calcBMR();
  if(bmr == null){ toast('Add your sex, age, and height in Profile first.'); return; }
  const weight = latestWeightKg();
  if(weight == null){ toast('Log your current weight in Progress first.'); return; }
  const tdee = calcTDEE();
  const p = STATE.profile;
  const dailyAdj = ((p.weeklyRateKg||0) * 7700) / 7;
  let calorieGoal = tdee;
  if(p.goalType === 'cut') calorieGoal = tdee - dailyAdj;
  else if(p.goalType === 'bulk') calorieGoal = tdee + dailyAdj;
  calorieGoal = Math.max(1200, Math.round(calorieGoal));
  const proteinPerKg = p.goalType === 'cut' ? 2.0 : 1.8;
  const proteinGoal = Math.round(weight * proteinPerKg);
  const fatGoal = Math.round(calorieGoal*0.25/9);
  const carbGoal = Math.max(0, Math.round((calorieGoal - proteinGoal*4 - fatGoal*9)/4));
  const fiberGoal = Math.round(calorieGoal/1000*14);
  STATE.goals.calorieGoal = calorieGoal;
  STATE.goals.proteinGoal = proteinGoal;
  STATE.goals.fatGoal = fatGoal;
  STATE.goals.carbGoal = carbGoal;
  STATE.goals.fiberGoal = fiberGoal;
  saveState();
  toast('Targets updated: '+calorieGoal+' kcal/day.');
  renderView();
}

/* ---------- App / view state ---------- */
let currentView = 'today';
let currentDate = todayKey();
let picker = null;
let mealBuilder = null;
let pendingCustomFoodBarcode = null;
let scanStream = null, scanDetector = null, scanning = false, lastScanResult = null;
let confirmCallback = null;
let weightChart = null;
let modalMode = null;

/* ---------- Toast ---------- */
function toast(msg){
  const wrap = document.getElementById('toastWrap');
  const el = document.createElement('div');
  el.className = 'toast'; el.textContent = msg;
  wrap.appendChild(el);
  requestAnimationFrame(()=> el.classList.add('show'));
  setTimeout(()=>{ el.classList.remove('show'); setTimeout(()=> el.remove(), 250); }, 2400);
}

/* ---------- Modal ---------- */
function openModalHtml(html, mode){
  modalMode = mode || 'generic';
  const overlay = document.getElementById('modalOverlay');
  document.getElementById('modalContent').innerHTML = html;
  overlay.classList.add('open');
}
function closeModal(){
  stopScan();
  const wasMealSlots = modalMode === 'meal-slots';
  document.getElementById('modalOverlay').classList.remove('open');
  document.getElementById('modalContent').innerHTML = '';
  picker = null; mealBuilder = null; pendingCustomFoodBarcode = null; modalMode = null;
  if(wasMealSlots) renderView();
}

/* ---------- Shell ---------- */
function renderNav(){
  const items = [
    ['progress', ICON.progress, 'Progress'],
    ['foods', ICON.foods, 'Food'],
    ['today', ICON.home, 'Home'],
    ['nutrients', ICON.nutrients, 'Nutrients'],
    ['profile', ICON.profile, 'Profile'],
  ];
  return items.map(([id,icon,label])=>
    `<button class="nav-item ${currentView===id?'active':''}" data-action="nav" data-view="${id}">${icon}<span>${label}</span></button>`
  ).join('');
}
function renderThemeButtons(){
  const t = STATE.goals.theme || 'system';
  return ['light','dark','system'].map(v=>
    `<button class="theme-btn ${t===v?'active':''}" data-action="set-theme" data-theme="${v}">${v[0].toUpperCase()+v.slice(1)}</button>`
  ).join('');
}
function renderShell(){
  document.getElementById('sideNav').innerHTML = `
    <div class="brand"><span class="brand-mark">🍱</span><div><span class="brand-name">Tiffin</span><span class="brand-tag">track anything, anywhere</span></div></div>
    ${renderNav()}
    <div class="nav-spacer"></div>
    <div class="streak-pill">${ICON.flame}<span>${computeStreak()}-day streak</span></div>
    <div class="theme-row">${renderThemeButtons()}</div>
  `;
  document.getElementById('bottomNav').innerHTML = renderNav();
  document.getElementById('topbarTitle').textContent = ({progress:'Progress', foods:'Food', today:'Home', nutrients:'Nutrients', profile:'Profile'})[currentView];
}
function renderView(){
  const root = document.getElementById('viewRoot');
  let html = '';
  if(currentView === 'today') html = renderToday();
  else if(currentView === 'foods') html = renderFoodsView();
  else if(currentView === 'progress') html = renderProgressView();
  else if(currentView === 'nutrients') html = renderNutrientsView();
  else if(currentView === 'profile') html = renderProfileView();
  root.innerHTML = `<div class="fade-in">${html}</div>`;
  if(currentView === 'progress') ensureChartLoaded(renderWeightChartNow);
}
function renderApp(){ renderShell(); renderView(); }

const CHART_CDN_URL = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js';
let chartLoadState = 'unloaded';
function ensureChartLoaded(cb){
  if(typeof Chart !== 'undefined'){ chartLoadState = 'loaded'; cb(); return; }
  if(chartLoadState === 'error'){ cb(); return; }
  if(chartLoadState === 'loading'){
    const check = ()=>{ if(typeof Chart!=='undefined'){ cb(); } else if(chartLoadState==='loading'){ setTimeout(check,150); } else { cb(); } };
    setTimeout(check,150); return;
  }
  chartLoadState = 'loading';
  const s = document.createElement('script');
  s.src = CHART_CDN_URL;
  s.onload = ()=>{ chartLoadState='loaded'; cb(); };
  s.onerror = ()=>{ chartLoadState='error'; cb(); };
  document.head.appendChild(s);
}

/* ---------- Shared bits ---------- */
function dateNavHtml(){
  return `<div class="date-nav">
    <button class="btn-icon" data-action="date-prev">${ICON.chevLeft}</button>
    <div class="date-label">${fmtDateLabel(currentDate)}</div>
    <button class="btn-icon" data-action="date-next">${ICON.chevRight}</button>
  </div>`;
}
function ringSvg(pct, fillColor){
  const size=200, cx=size/2, cy=size/2, r=84;
  const circumference = 2*Math.PI*r;
  const p = clamp(pct,0,1);
  const dash = circumference*p;
  return `<svg viewBox="0 0 ${size} ${size}" style="transform:rotate(-90deg);">
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="var(--surface-2)" stroke-width="16"/>
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${fillColor}" stroke-width="16" stroke-linecap="round" stroke-dasharray="${dash} ${circumference}"/>
  </svg>`;
}
function barRow(label, consumed, goal, unit, opts){
  opts = opts || {};
  const pct = goal > 0 ? consumed/goal : 0;
  const over = opts.isLimit ? consumed > goal : pct > 1.02;
  const widthPct = clamp(pct,0,1)*100;
  return `<div class="nlabel-row">
    <div class="nlabel-top">
      <span class="name">${label}</span>
      <span class="vals">${round1(consumed)}${unit} / ${goal ? round1(goal)+unit : '—'}</span>
    </div>
    <div class="bar-track"><div class="bar-fill ${over?'over':''}" style="width:${widthPct}%"></div></div>
  </div>`;
}
function qtyLabelFor(base, qty){
  const grams = Math.round((base.servingGrams||0) * qty);
  const label = escapeHtml(base.servingLabel);
  if(Math.abs(qty-1) < 0.001) return `${label} · ${grams} g`;
  const qtyStr = (Math.round(qty*100)/100).toString();
  return `${qtyStr} × ${label} · ${grams} g`;
}
const SIZE_MULT = {small:0.75, medium:1, large:1.5};
function computeGrams(base, unit, amount){
  if(unit === 'grams') return amount;
  return amount * SIZE_MULT[unit] * base.servingGrams;
}
function defaultAmountForUnit(base, unit, grams){
  if(unit === 'grams') return Math.round(grams);
  const mult = SIZE_MULT[unit];
  return round1(grams / (mult * base.servingGrams)) || 1;
}

/* ---------- Today (Home) ---------- */
function renderToday(){
  const totals = dayTotals(currentDate);
  const g = STATE.goals;
  const kcalPct = g.calorieGoal>0 ? totals.kcal/g.calorieGoal : 0;
  const remaining = Math.round(g.calorieGoal - totals.kcal);
  const fillColor = kcalPct > 1.02 ? 'var(--warn)' : 'var(--accent)';
  const name = (STATE.profile.name||'').trim();

  const macroRows = [
    barRow('Protein', totals.protein, g.proteinGoal, 'g'),
    barRow('Carbs', totals.carbs, g.carbGoal, 'g'),
    barRow('Fat', totals.fat, g.fatGoal, 'g'),
  ].join('');

  const miniStats = `<div class="mini-stat-grid">
    <div class="mini-stat"><div class="val">${round1(totals.fiber)}g</div><div class="lbl">Fiber</div></div>
    <div class="mini-stat"><div class="val">${round1(totals.sugar)}g</div><div class="lbl">Sugar</div></div>
    <div class="mini-stat"><div class="val">${Math.round(totals.sodium)}mg</div><div class="lbl">Sodium</div></div>
  </div>`;

  const mealSections = STATE.mealSlots.map(slot=>{
    const day = getDay(currentDate);
    const items = day[slot.id] || [];
    const mt = mealTotal(currentDate, slot.id);
    const rows = items.length ? items.map((entry,idx)=>{
      const base = resolveRefBase(entry.ref);
      if(!base) return '';
      const n = entryNutrients(entry);
      return `<div class="meal-item" data-action="edit-entry" data-meal="${escapeHtml(slot.id)}" data-index="${idx}">
        <div class="info" style="flex:1;"><div class="name">${escapeHtml(base.name)}</div><div class="qty">${qtyLabelFor(base, entry.qty)}</div></div>
        <div class="kcal">${Math.round(n.kcal)}</div>
        <span class="icon-x" data-action="delete-entry" data-meal="${escapeHtml(slot.id)}" data-index="${idx}" title="Remove">${ICON.x}</span>
      </div>`;
    }).join('') : `<div class="meal-empty">Nothing logged yet.</div>`;
    return `<div class="meal-card">
      <div class="meal-head">
        <h3><span class="emoji">${escapeHtml(slot.emoji)}</span> ${escapeHtml(slot.name)}</h3>
        <div class="meal-macros">
          <span class="mk">${Math.round(mt.kcal)} kcal</span>
          <span>P ${round1(mt.protein)}g</span>
          <span>C ${round1(mt.carbs)}g</span>
          <span>F ${round1(mt.fat)}g</span>
        </div>
      </div>
      ${rows}
      <div class="meal-add-link" data-action="open-picker" data-meal="${escapeHtml(slot.id)}">${ICON.plus} Add ${escapeHtml(slot.name)}</div>
    </div>`;
  }).join('');

  return `
    <div class="home-header">
      <div class="greeting">${name ? `Hi, ${escapeHtml(name)} 👋` : 'Welcome back 👋'}</div>
      <div class="streak-pill" style="margin:0;">${ICON.flame}<span>${computeStreak()}-day streak</span></div>
    </div>
    ${dateNavHtml()}
    <div class="card">
      <div class="ring-section">
        <div class="ring-wrap" data-action="open-energy-modal">
          ${ringSvg(kcalPct, fillColor)}
          <div class="ring-center">
            <div class="ring-num">${Math.abs(remaining)}</div>
            <div class="ring-sub">${remaining>=0 ? 'kcal left' : 'kcal over'}</div>
            <div class="ring-sub2">${Math.round(totals.kcal)} / ${g.calorieGoal}</div>
          </div>
        </div>
        <div class="ring-hint">Tap for energy breakdown</div>
      </div>
      <div class="macro-rows">${macroRows}</div>
      ${miniStats}
    </div>
    ${waterCardHtml()}
    ${workoutCardHtml()}
    <div class="section-head"><h2>Meals</h2><button class="btn-icon" data-action="open-meal-slots" title="Edit meals">${ICON.pencil}</button></div>
    ${mealSections}
    <button class="fab-scan" data-action="open-scan-modal" title="Scan barcode">${ICON.scan}</button>
  `;
}

/* ---------- Water ---------- */
function waterCardHtml(){
  const day = getDay(currentDate);
  const goal = STATE.goals.waterGoalMl || 2500;
  const ml = day.water || 0;
  const glassSize = 250;
  const totalGlasses = Math.max(6, Math.ceil(goal/glassSize));
  const filled = Math.round(ml/glassSize);
  const glasses = Array.from({length: totalGlasses}, (_,i)=>
    `<button type="button" class="glass-btn ${i<filled?'filled':''}" data-action="set-water-glass" data-index="${i}" title="${(i+1)*glassSize} ml">🥛</button>`
  ).join('');
  return `<div class="card">
    <div class="section-head" style="margin:0 0 10px;"><h2>Water</h2><span class="meta">${ml} / ${goal} ml</span></div>
    <div class="glass-grid">${glasses}</div>
    <div class="water-quick">
      <button class="btn btn-outline btn-sm" data-action="add-water" data-ml="250">+1 glass</button>
      <button class="btn btn-outline btn-sm" data-action="add-water" data-ml="500">+500 ml</button>
      <button class="btn btn-outline btn-sm" data-action="add-water" data-ml="1000">+1 L</button>
      <input type="number" id="waterCustomInput" placeholder="ml" style="max-width:80px;">
      <button class="btn btn-outline btn-sm" data-action="add-water-custom">Add</button>
      <button class="btn btn-ghost btn-sm" data-action="reset-water">Reset</button>
    </div>
  </div>`;
}

/* ---------- Workout ---------- */
function workoutCardHtml(){
  const day = getDay(currentDate);
  const list = day.workouts || [];
  const rows = list.length ? list.map((w,idx)=>`<div class="meal-item"><div class="info" style="flex:1;"><div class="name">${escapeHtml(w.name)}</div><div class="qty">${w.duration?w.duration+' min':''}</div></div><span class="icon-x" data-action="delete-workout" data-index="${idx}">${ICON.x}</span></div>`).join('') : `<div class="meal-empty">No workouts logged today.</div>`;
  const cells = [];
  for(let i=13;i>=0;i--){
    const k = addDaysKey(todayKey(), -i);
    const has = STATE.diary[k] && Array.isArray(STATE.diary[k].workouts) && STATE.diary[k].workouts.length>0;
    cells.push(`<div class="heatmap-cell ${has?'on':''}" title="${k}"></div>`);
  }
  return `<div class="card">
    <div class="section-head" style="margin:0 0 10px;"><h2>Workout</h2></div>
    <form id="workoutForm" class="field-row" style="align-items:flex-end;">
      <div class="field" style="flex:1;"><label>Activity</label><input type="text" name="name" placeholder="e.g. Gym, Run" required></div>
      <div class="field" style="width:90px;"><label>Minutes</label><input type="number" name="duration" min="0"></div>
      <button type="submit" class="btn btn-primary">Log</button>
    </form>
    ${rows}
    <div class="heatmap-row" style="margin-top:10px;">${cells.join('')}</div>
    <div class="muted" style="font-size:11px;">Last 14 days</div>
  </div>`;
}

/* ---------- Energy modal ---------- */
function openEnergyModal(){
  const totals = dayTotals(currentDate);
  const consumed = totals.kcal;
  const target = STATE.goals.calorieGoal;
  const bmr = calcBMR();
  const tdee = calcTDEE();
  let body;
  if(bmr == null){
    const diff = consumed - target;
    body = `
      <div class="modal-head"><h3>Energy breakdown</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
      <p class="muted" style="font-size:13.5px;">Add your sex, age, height and activity level in Profile to see the full breakdown (baseline burn, activity, and food digestion).</p>
      <div class="energy-row total"><span>Energy Target</span><span class="v">${target} kcal</span></div>
      <div class="energy-row"><span>Consumed</span><span class="v">${Math.round(consumed)} kcal</span></div>
      <div class="energy-row balance"><span>${diff>0?'Over target':'Under target'}</span><span class="v ${diff>0?'over':'under'}">${Math.abs(Math.round(diff))} kcal</span></div>
      <button class="btn btn-outline" style="width:100%;margin-top:14px;" data-action="goto-profile-from-modal">Go to Profile</button>
    `;
  } else {
    const above = tdee - bmr;
    const tef = consumed * 0.1;
    const totalTarget = tdee + tef;
    const diff = consumed - totalTarget;
    body = `
      <div class="modal-head"><h3>Energy breakdown</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
      <div class="energy-row"><span>Energy Target</span><span class="v">${Math.round(target)} kcal</span></div>
      <div class="energy-row"><span>Baseline (BMR)</span><span class="v">${Math.round(bmr)} kcal</span></div>
      <div class="energy-row"><span>Expenditure above baseline</span><span class="v">+${Math.round(above)} kcal</span></div>
      <div class="energy-row"><span>TEF (food digestion, ~10%)</span><span class="v">+${Math.round(tef)} kcal</span></div>
      <div class="energy-row total"><span>Total Target (burned today)</span><span class="v">${Math.round(totalTarget)} kcal</span></div>
      <div class="energy-row"><span>Consumed</span><span class="v">${Math.round(consumed)} kcal</span></div>
      <div class="energy-row balance"><span>${diff>0?'Over':'Under'} total burn</span><span class="v ${diff>0?'over':'under'}">${Math.abs(Math.round(diff))} kcal</span></div>
      <div class="disclaimer">Estimated with the Mifflin-St Jeor formula and your activity level — actual needs vary. Not medical advice.</div>
    `;
  }
  openModalHtml(body, 'generic');
}

/* ---------- Nutrients tab ---------- */
function renderNutrientsView(){
  const totals = dayTotals(currentDate);
  const G = Object.assign({}, FIXED_TARGETS, STATE.goals);
  const groups = NUTRIENT_GROUPS.map(grp=>{
    const rows = grp.rows.map(([key,label,unit,goalKey,isLimit])=>{
      const goal = goalKey ? G[goalKey] : null;
      return barRow(label, totals[key]||0, goal, ' '+unit, {isLimit});
    }).join('');
    return `<div class="nutrient-group-title">${grp.title}</div><div style="display:flex;flex-direction:column;gap:16px;">${rows}</div>`;
  }).join('');
  return `
    ${dateNavHtml()}
    <div class="card">
      <h2 style="margin-bottom:4px;">Today's nutrients</h2>
      <div class="muted" style="font-size:12px;margin-bottom:6px;">Calories: ${Math.round(totals.kcal)} kcal</div>
      ${groups}
      <div class="disclaimer">Values are estimated from standard food-composition heuristics, not lab measurements. A few highly specialised markers — individual amino acids (leucine, EAAs, BCAAs), creatine beyond meat/fish, and melatonin — aren't tracked, since reliable per-food data for these doesn't exist in standard nutrition databases either. Targets are general adult reference values, not personalised medical advice.</div>
    </div>
  `;
}

/* ---------- Foods view ---------- */
let foodsFilter = {query:'', cat:'All'};
function allBrowsable(){
  const list = [];
  // Custom foods/meals first: the food-row list is capped (see foodRowsHtml),
  // and with 332+ DB items ahead of them, a user's own foods could otherwise
  // fall outside that cap and never show up in the default "All" view.
  STATE.customFoods.forEach(f=> list.push({ref:{type:'custom', id:f.id}, name:f.name, servingLabel:f.servingLabel, kcal:f.kcal, category:'Custom'}));
  STATE.customMeals.forEach(m=>{
    const base = resolveRefBase({type:'meal', id:m.id});
    list.push({ref:{type:'meal', id:m.id}, name:m.name, servingLabel:'1 recipe', kcal: base? base.nutrients.kcal : 0, category:'Meal'});
  });
  FOOD_DB.forEach(f=> list.push({ref:{type:'db', id:f.id}, name:f.name, servingLabel:f.servingLabel, kcal:f.kcal, category:f.category}));
  return list;
}
function filterFoods(list, query, cat){
  const q = query.trim().toLowerCase();
  return list.filter(item=>{
    if(cat !== 'All' && item.category !== cat) return false;
    if(q && !item.name.toLowerCase().includes(q)) return false;
    return true;
  });
}
function foodRowsHtml(list, opts){
  opts = opts || {};
  const mode = opts.mode || 'pick';
  if(!list.length) return `<div class="empty-state"><div class="big">🍽️</div>No foods match — try another search, or create a custom food.</div>`;
  return list.slice(0,200).map(item=>{
    const tagClass = item.category==='Indian'?'indian':(item.category==='International'?'international':'custom');
    const action = mode==='link' ? 'pick-link' : (mode==='quickadd' ? 'quick-add' : 'select-food');
    const canDelete = opts.allowDelete && (item.ref.type === 'custom' || item.ref.type === 'meal');
    const deleteBtn = canDelete
      ? `<span class="icon-x" data-action="${item.ref.type==='meal'?'delete-custom-meal':'delete-custom-food'}" data-id="${escapeHtml(item.ref.id)}" title="Delete">${ICON.x}</span>`
      : '';
    return `<div class="food-row" data-action="${action}" data-ref-type="${item.ref.type}" data-ref-id="${escapeHtml(item.ref.id)}">
      <div class="info">
        <div class="fname">${escapeHtml(item.name)}</div>
        <div class="fserv">${escapeHtml(item.servingLabel)}</div>
      </div>
      <span class="tag ${tagClass}">${item.category}</span>
      <span class="fkcal">${Math.round(item.kcal)}</span>
      ${deleteBtn}
    </div>`;
  }).join('');
}
function renderFoodsView(){
  const list = filterFoods(allBrowsable(), foodsFilter.query, foodsFilter.cat);
  const cats = ['All','Indian','International','Custom','Meal'];
  return `
    <div class="row between" style="margin-bottom:14px;flex-wrap:wrap;gap:8px;">
      <button class="btn btn-outline btn-sm" data-action="open-custom-food">${ICON.plus} Custom food</button>
      <button class="btn btn-outline btn-sm" data-action="open-custom-meal">${ICON.plus} Custom meal</button>
    </div>
    <div class="search-input"><input type="text" id="foodsSearch" placeholder="Search foods..." value="${escapeHtml(foodsFilter.query)}"></div>
    <div class="chip-row" style="margin-bottom:12px;">${cats.map(c=>`<button class="chip ${foodsFilter.cat===c?'active':''}" data-action="foods-filter-cat" data-cat="${c}">${c==='Meal'?'My meals':c}</button>`).join('')}</div>
    <div class="food-list" id="foodsList">${foodRowsHtml(list,{mode:'quickadd', allowDelete:true})}</div>
  `;
}

/* ---------- Picker (add-one-at-a-time, then Finish) ---------- */
function openPicker(opts){
  picker = Object.assign({
    step:'list', query:'', cat:'All', meal:null, dateKey:currentDate,
    cart: [], activeRef:null, activeUnit:'medium', activeAmount:1,
    linkOnly:false, pendingBarcode:null, editMeal:null, editIndex:null, singleMode:false
  }, opts||{});
  renderPickerModal();
}
function renderPickerModal(){
  if(!picker) return;
  const html = picker.step === 'list' ? renderListStep() : renderServingStep();
  openModalHtml(html, 'generic');
}
function renderListStep(){
  const list = filterFoods(allBrowsable(), picker.query, picker.cat);
  const cats = ['All','Indian','International','Custom','Meal'];
  const cartRows = picker.cart.map((item,idx)=>{
    const base = resolveRefBase(item.ref);
    if(!base) return '';
    const qty = base.servingGrams>0 ? item.grams/base.servingGrams : 1;
    const n = scaleNutrients(base.nutrients, qty);
    return `<div class="meal-item"><div class="info" style="flex:1;"><div class="name">${escapeHtml(base.name)}</div><div class="qty">${Math.round(item.grams)} g</div></div><div class="kcal">${Math.round(n.kcal)}</div><span class="icon-x" data-action="cart-remove" data-index="${idx}">${ICON.x}</span></div>`;
  }).join('');
  const footer = (!picker.linkOnly && picker.cart.length>0)
    ? `<div class="picker-footer"><span>${picker.cart.length} added</span><button class="btn btn-primary btn-sm" data-action="picker-finish">Finish</button></div>` : '';
  return `
    <div class="modal-head"><h3>${picker.linkOnly? 'Link barcode to a food' : (picker.meal? 'Add to '+mealName(picker.meal) : 'Add food')}</h3>
      <button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    ${!picker.linkOnly ? `<div class="field-hint" style="margin-bottom:10px;">Tap a food to set its serving, then add another or hit Finish.</div>` : ''}
    <div class="search-input"><input type="text" id="pickerSearch" placeholder="Search foods..." value="${escapeHtml(picker.query)}" autofocus></div>
    <div class="chip-row" style="margin-bottom:10px;">${cats.map(c=>`<button class="chip ${picker.cat===c?'active':''}" data-action="picker-filter-cat" data-cat="${c}">${c==='Meal'?'My meals':c}</button>`).join('')}</div>
    <div class="food-list" id="pickerList">${foodRowsHtml(list,{mode:picker.linkOnly?'link':'pick'})}</div>
    <div class="row" style="justify-content:center;margin-top:14px;">
      <button class="btn btn-ghost btn-sm" data-action="open-custom-food">${ICON.plus} New custom food</button>
    </div>
    ${picker.cart.length>0 ? `<div class="section-head" style="margin:18px 0 4px;"><h2 style="font-size:14px;">Added so far</h2></div>${cartRows}` : ''}
    ${footer}
  `;
}
function renderServingStep(){
  const base = resolveRefBase(picker.activeRef);
  if(!base){ picker.step = 'list'; return renderListStep(); }
  const grams = computeGrams(base, picker.activeUnit, picker.activeAmount);
  const qty = base.servingGrams>0 ? grams/base.servingGrams : 1;
  const n = scaleNutrients(base.nutrients, qty);
  const units = [['grams','Grams'],['small','Small'],['medium','Medium'],['large','Large']];
  const mealOptions = STATE.mealSlots.map(s=>`<option value="${escapeHtml(s.id)}" ${picker.meal===s.id?'selected':''}>${escapeHtml(s.name)}</option>`).join('');
  const isEdit = picker.editMeal != null;
  const primaryAction = (picker.singleMode || isEdit) ? 'commit-single' : 'add-to-cart';
  const primaryLabel = isEdit ? 'Save' : (picker.singleMode ? 'Add' : 'Add to list');
  return `
    <div class="modal-head"><h3>${escapeHtml(base.name)}</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    <div class="muted" style="font-size:12.5px;margin-bottom:14px;">${escapeHtml(base.servingLabel)} = ${Math.round(base.servingGrams)} g</div>
    <div class="field"><label>Serving size</label>
      <div class="chip-row">${units.map(([u,label])=>`<button type="button" class="chip ${picker.activeUnit===u?'active':''}" data-action="set-serving-unit" data-unit="${u}">${label}</button>`).join('')}</div>
    </div>
    <div class="field"><label>Amount ${picker.activeUnit==='grams' ? '(grams)' : '('+picker.activeUnit+' servings)'}</label>
      <input type="number" id="servingAmount" value="${picker.activeAmount}" min="0.1" step="${picker.activeUnit==='grams'?1:0.5}" inputmode="decimal">
    </div>
    ${!picker.meal ? `<div class="field"><label>Meal</label><select id="pickerMealSelect">${mealOptions}</select></div>` : `<div class="field-hint" style="margin-bottom:10px;">Adding to ${escapeHtml(mealEmoji(picker.meal))} ${escapeHtml(mealName(picker.meal))}</div>`}
    <div class="grid-2" style="margin:14px 0;">
      <div class="stat-block"><div class="label">Calories</div><div class="value" id="servingKcal">${Math.round(n.kcal)}</div></div>
      <div class="stat-block"><div class="label">Protein</div><div class="value" id="servingProtein">${round1(n.protein)}g</div></div>
      <div class="stat-block"><div class="label">Carbs</div><div class="value" id="servingCarbs">${round1(n.carbs)}g</div></div>
      <div class="stat-block"><div class="label">Fat</div><div class="value" id="servingFat">${round1(n.fat)}g</div></div>
    </div>
    <div class="row gap-8">
      ${(!isEdit && !picker.singleMode) ? `<button class="btn btn-outline" data-action="serving-cancel">Back</button>` : ''}
      <button class="btn btn-primary" style="flex:1;" data-action="${primaryAction}">${ICON.plus} ${primaryLabel}</button>
    </div>
  `;
}

/* ---------- Custom food form ---------- */
// kcal/protein/carbs/fat are the always-visible primary fields below; every
// other NUTRIENT_KEYS entry gets a field here, grouped exactly like the
// Nutrients tab (NUTRIENT_GROUPS), so a supplement's label -- vitamin D,
// magnesium, creatine, whatever -- can always be entered somewhere.
const CUSTOM_FOOD_PRIMARY_KEYS = ['protein','carbs','fat'];
function customFoodNutrientFieldsHtml(){
  return NUTRIENT_GROUPS.map(grp=>{
    const rows = grp.rows.filter(([key])=> !CUSTOM_FOOD_PRIMARY_KEYS.includes(key));
    if(!rows.length) return '';
    let pairsHtml = '';
    for(let i=0;i<rows.length;i+=2){
      const fields = rows.slice(i,i+2).map(([key,label,unit])=>
        `<div class="field"><label>${escapeHtml(label)} (${escapeHtml(unit)})</label><input type="number" name="${key}" value="0" min="0" step="0.01"></div>`
      ).join('');
      pairsHtml += `<div class="field-row">${fields}</div>`;
    }
    return `<details class="settings-group"><summary>${escapeHtml(grp.title)}</summary>${pairsHtml}</details>`;
  }).join('');
}
function openCustomFoodForm(){
  const bc = pendingCustomFoodBarcode;
  const html = `
    <div class="modal-head"><h3>New custom food</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    ${bc ? `<div class="field-hint" style="margin-bottom:10px;">Will be linked to scanned barcode ${escapeHtml(bc)}</div>` : ''}
    <form id="customFoodForm">
      <div class="field"><label>Name</label><input required type="text" name="name" placeholder="e.g. Mum's chicken curry"></div>
      <div class="field-row">
        <div class="field"><label>Serving label</label><input type="text" name="servingLabel" value="1 serving"></div>
        <div class="field"><label>Serving size (g)</label><input type="number" name="servingGrams" value="100" min="1"></div>
      </div>
      <div class="field-row">
        <div class="field"><label>Calories</label><input required type="number" name="kcal" value="0" min="0"></div>
        <div class="field"><label>Protein (g)</label><input type="number" name="protein" value="0" min="0" step="0.1"></div>
      </div>
      <div class="field-row">
        <div class="field"><label>Carbs (g)</label><input type="number" name="carbs" value="0" min="0" step="0.1"></div>
        <div class="field"><label>Fat (g)</label><input type="number" name="fat" value="0" min="0" step="0.1"></div>
      </div>
      <div class="field-hint" style="margin:-6px 0 10px;">The groups below match the Nutrients tab — fill in whatever's on the label (a supplement's vitamin D, magnesium, creatine dose, etc.). Anything left at 0 just won't count toward that nutrient's total.</div>
      ${customFoodNutrientFieldsHtml()}
      <button type="submit" class="btn btn-primary" style="width:100%;margin-top:6px;">Save custom food</button>
    </form>
  `;
  openModalHtml(html, 'generic');
}
function handleCustomFoodSubmit(form){
  const fd = new FormData(form);
  const name = (fd.get('name')||'').toString().trim();
  if(!name){ toast('Please name this food.'); return; }
  const num = (k, d)=>{ const v = parseFloat(fd.get(k)); return isNaN(v) ? d : v; };
  const id = 'custom-'+uid();
  const food = {
    id, name, category:'Custom',
    servingLabel: (fd.get('servingLabel')||'1 serving').toString().trim() || '1 serving',
    servingGrams: num('servingGrams',100),
  };
  NUTRIENT_KEYS.forEach(k=> food[k] = num(k, 0));
  STATE.customFoods.push(food);
  let msg = 'Custom food added.';
  if(pendingCustomFoodBarcode){
    STATE.barcodeMap[pendingCustomFoodBarcode] = {type:'custom', id};
    msg = 'Custom food added and linked to barcode.';
  }
  saveState();
  closeModal();
  toast(msg);
  renderView();
}

/* ---------- Custom meal builder ---------- */
function openCustomMealForm(){
  mealBuilder = {name:'', items:[], query:''};
  renderMealBuilderModal();
}
function renderMealBuilderModal(){
  if(!mealBuilder) return;
  const matches = mealBuilder.query.trim() ? filterFoods(allBrowsable(), mealBuilder.query, 'All').filter(i=>i.ref.type!=='meal').slice(0,8) : [];
  let total = zeroNutrients();
  mealBuilder.items.forEach(it=>{ const b = resolveRefBase(it.ref); if(b) total = addNutrients(total, scaleNutrients(b.nutrients, it.qty)); });
  const itemRows = mealBuilder.items.map((it,idx)=>{
    const b = resolveRefBase(it.ref);
    if(!b) return '';
    return `<div class="meal-item">
      <div class="info" style="flex:1;"><div class="name">${escapeHtml(b.name)}</div><div class="qty">${qtyLabelFor(b, it.qty)}</div></div>
      <div class="kcal">${Math.round(scaleNutrients(b.nutrients,it.qty).kcal)}</div>
      <span class="icon-x" data-action="remove-meal-item" data-index="${idx}">${ICON.x}</span>
    </div>`;
  }).join('') || `<div class="meal-empty">No ingredients yet — search below to add some.</div>`;
  const matchRows = matches.length ? matches.map(m=>`<div class="food-row" data-action="add-meal-item" data-ref-type="${m.ref.type}" data-ref-id="${escapeHtml(m.ref.id)}">
      <div class="info"><div class="fname">${escapeHtml(m.name)}</div><div class="fserv">${escapeHtml(m.servingLabel)}</div></div>
      <span class="fkcal">${Math.round(m.kcal)}</span>
    </div>`).join('') : '';
  const html = `
    <div class="modal-head"><h3>New custom meal</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    <div class="field"><label>Meal name</label><input type="text" id="mealBuilderName" placeholder="e.g. My protein breakfast bowl" value="${escapeHtml(mealBuilder.name)}"></div>
    <div style="margin-bottom:6px;font-size:12.5px;font-weight:700;color:var(--text-muted);">Ingredients (${Math.round(total.kcal)} kcal total)</div>
    <div class="food-list" style="max-height:26vh;margin-bottom:10px;">${itemRows}</div>
    <div class="search-input"><input type="text" id="mealBuilderSearch" placeholder="Search to add an ingredient..." value="${escapeHtml(mealBuilder.query)}"></div>
    ${matches.length ? `<div class="food-list" style="max-height:22vh;">${matchRows}</div>` : ''}
    <button class="btn btn-primary" style="width:100%;margin-top:14px;" data-action="save-custom-meal">Save meal</button>
  `;
  openModalHtml(html, 'generic');
}

/* ---------- Meal slot manager ---------- */
function openMealSlotsModal(){ renderMealSlotsModal(); }
function renderMealSlotsModal(){
  const rows = STATE.mealSlots.map((s,idx)=>`
    <div class="slot-row">
      <button class="emoji-btn" data-action="slot-cycle-emoji" data-id="${escapeHtml(s.id)}">${escapeHtml(s.emoji)}</button>
      <input type="text" data-slot-name="${escapeHtml(s.id)}" value="${escapeHtml(s.name)}" placeholder="Meal name">
      <div class="slot-reorder">
        <button data-action="slot-move-up" data-index="${idx}" ${idx===0?'disabled':''}>${ICON.chevUp}</button>
        <button data-action="slot-move-down" data-index="${idx}" ${idx===STATE.mealSlots.length-1?'disabled':''}>${ICON.chevDown}</button>
      </div>
      <span class="icon-x" data-action="slot-delete" data-index="${idx}" title="Delete">${ICON.x}</span>
    </div>
  `).join('');
  openModalHtml(`
    <div class="modal-head"><h3>Edit meals</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    <div class="field-hint" style="margin-bottom:6px;">Tap the emoji to cycle icons. Deleting a meal also removes anything logged under it.</div>
    <div>${rows}</div>
    <button class="add-link" style="margin-top:14px;" data-action="slot-add">${ICON.plus} Add another meal</button>
    <button class="btn btn-primary" style="width:100%;margin-top:18px;" data-action="close-modal">Done</button>
  `, 'meal-slots');
}

/* ---------- Progress view ---------- */
function renderProgressView(){
  const log = [...STATE.weightLog].sort((a,b)=> a.date < b.date ? -1 : 1);
  const unit = weightUnitLabel();
  const g = STATE.goals;
  const current = log.length ? log[log.length-1].kg : null;
  const start = g.startWeightKg != null ? g.startWeightKg : (log.length ? log[0].kg : null);
  let deltaHtml = '';
  if(current != null && start != null){
    const d = current - start;
    const cls = d <= 0 ? 'down' : 'up';
    deltaHtml = `<div class="delta ${cls}">${d<=0?'':'+'}${round1(toDisplayWeight(d))} ${unit} since start</div>`;
  }
  const cells = [];
  for(let i=83;i>=0;i--){ const k = addDaysKey(todayKey(), -i); cells.push({key:k, has: dayHasEntries(k)}); }
  const heat = cells.map(c=>`<div class="heatmap-cell ${c.has?'on':''}" title="${c.key}"></div>`).join('');

  return `
    <div class="card">
      <div class="stat-pair">
        <div class="stat-block"><div class="label">Current</div><div class="value">${current!=null? round1(toDisplayWeight(current))+' '+unit : '—'}</div></div>
        <div class="stat-block"><div class="label">Goal</div><div class="value">${g.weightGoalKg!=null? round1(toDisplayWeight(g.weightGoalKg))+' '+unit : 'Not set'}</div>${deltaHtml}</div>
      </div>
      <div class="chart-wrap"><canvas id="weightChart"></canvas></div>
    </div>
    <div class="section-head"><h2>Log weight</h2></div>
    <div class="card">
      <form id="weightForm" class="field-row" style="align-items:flex-end;">
        <div class="field" style="flex:1;"><label>Date</label><input type="date" name="date" value="${todayKey()}" max="${todayKey()}"></div>
        <div class="field" style="flex:1;"><label>Weight (${unit})</label><input type="number" name="weight" step="0.1" min="0" required></div>
        <button type="submit" class="btn btn-primary">Save</button>
      </form>
      ${log.length ? [...log].reverse().slice(0,10).map(w=>{
        const realIdx = STATE.weightLog.findIndex(x=>x.date===w.date);
        return `<div class="weight-log-row"><span class="d">${w.date}</span><span>${round1(toDisplayWeight(w.kg))} ${unit}</span><span class="icon-x" data-action="delete-weight" data-index="${realIdx}">${ICON.x}</span></div>`;
      }).join('') : `<div class="muted" style="font-size:13px;margin-top:10px;">No weigh-ins logged yet.</div>`}
    </div>
    <div class="section-head"><h2>Logging streak</h2><span class="meta">${computeStreak()} days</span></div>
    <div class="card"><div class="heatmap">${heat}</div><div class="muted" style="font-size:11.5px;">Last 12 weeks — filled squares are days with at least one food logged.</div></div>
  `;
}
function renderWeightChartNow(){
  const canvas = document.getElementById('weightChart');
  if(!canvas) return;
  if(typeof Chart === 'undefined'){
    canvas.replaceWith(Object.assign(document.createElement('div'),{className:'muted',textContent:'Chart unavailable — see the weigh-in list below.'}));
    return;
  }
  const log = [...STATE.weightLog].sort((a,b)=> a.date < b.date ? -1 : 1);
  const labels = log.map(w=>w.date.slice(5));
  const data = log.map(w=> round1(toDisplayWeight(w.kg)));
  const goal = STATE.goals.weightGoalKg;
  const textColor = css('--text-muted') || '#8C7F68';
  const gridColor = css('--border') || '#E7DAC0';
  const accentColor = css('--accent') || '#FF6B4A';
  if(weightChart){ weightChart.destroy(); weightChart = null; }
  try{
    weightChart = new Chart(canvas.getContext('2d'), {
      type:'line',
      data:{ labels, datasets:[
        {label:'Weight', data, borderColor:accentColor, backgroundColor:accentColor+'22', tension:.3, pointRadius:3, fill:true},
        ...(goal!=null ? [{label:'Goal', data: labels.map(()=> round1(toDisplayWeight(goal))), borderColor:textColor, borderDash:[6,4], pointRadius:0}] : [])
      ]},
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{legend:{labels:{color:textColor}}},
        scales:{ x:{ticks:{color:textColor}, grid:{color:gridColor}}, y:{ticks:{color:textColor}, grid:{color:gridColor}} } }
    });
  }catch(e){}
}

/* ---------- Profile view ---------- */
function renderProfileView(){
  const g = STATE.goals;
  const p = STATE.profile;
  const unit = weightUnitLabel();
  return `
    <div class="section-head"><h2>Profile</h2></div>
    <form id="profileForm" class="card">
      <div class="field"><label>Your name</label><input type="text" name="name" value="${escapeHtml(p.name||'')}" placeholder="Optional — shows on the Home greeting"></div>
      <button type="submit" class="btn btn-primary">Save</button>
    </form>

    <div class="section-head"><h2>Body & goal</h2></div>
    <form id="bodyForm" class="card">
      <div class="field-row">
        <div class="field"><label>Sex (for energy calc)</label>
          <div class="chip-row">
            <button type="button" class="chip ${p.sex==='male'?'active':''}" data-action="set-sex" data-sex="male">Male</button>
            <button type="button" class="chip ${p.sex==='female'?'active':''}" data-action="set-sex" data-sex="female">Female</button>
          </div>
        </div>
        <div class="field"><label>Age</label><input type="number" name="age" value="${p.age||''}" min="10" max="100"></div>
      </div>
      <div class="field-row">
        <div class="field">
          <label>Height</label>
          <div class="chip-row" style="margin-bottom:6px;">
            <button type="button" class="chip ${(p.heightUnit||'cm')==='cm'?'active':''}" data-action="set-height-unit" data-unit="cm">cm</button>
            <button type="button" class="chip ${(p.heightUnit||'cm')==='ft'?'active':''}" data-action="set-height-unit" data-unit="ft">ft/in</button>
          </div>
          ${(p.heightUnit||'cm')==='cm'
            ? `<input type="number" name="heightCm" value="${p.heightCm||''}" min="100" max="250" placeholder="cm">`
            : `<div class="field-row"><input type="number" name="heightFt" value="${p.heightCm? Math.floor(p.heightCm/2.54/12):''}" min="3" max="8" placeholder="ft"><input type="number" name="heightIn" value="${p.heightCm? Math.round(p.heightCm/2.54)%12:''}" min="0" max="11" placeholder="in"></div>`}
        </div>
        <div class="field"><label>Activity level</label>
          <select name="activityLevel">${Object.keys(ACTIVITY_MULT).map(k=>`<option value="${k}" ${p.activityLevel===k?'selected':''}>${ACTIVITY_LABEL[k]}</option>`).join('')}</select>
        </div>
      </div>
      <div class="field"><label>Goal</label>
        <div class="chip-row">
          <button type="button" class="chip ${p.goalType==='cut'?'active':''}" data-action="set-goal-type" data-goal="cut">Lose weight</button>
          <button type="button" class="chip ${p.goalType==='maintain'?'active':''}" data-action="set-goal-type" data-goal="maintain">Maintain</button>
          <button type="button" class="chip ${p.goalType==='bulk'?'active':''}" data-action="set-goal-type" data-goal="bulk">Gain weight</button>
        </div>
      </div>
      ${p.goalType !== 'maintain' ? `
      <div class="field"><label>Target weekly ${p.goalType==='cut'?'loss':'gain'}</label>
        <div class="chip-row">
          ${[0.25,0.5,0.75,1].map(v=>`<button type="button" class="chip ${Math.abs((p.weeklyRateKg||0)-v)<0.01?'active':''}" data-action="set-weekly-rate" data-rate="${v}">${v<1?Math.round(v*1000)+' g':v+' kg'}</button>`).join('')}
        </div>
        <div class="field-hint">1 kg/week isn't usually recommended without medical guidance — use it only under professional advice.</div>
      </div>` : ''}
      <div class="field"><label>Daily water goal (ml)</label><input type="number" name="waterGoalMl" value="${g.waterGoalMl}" min="500" step="50"></div>
      <button type="submit" class="btn btn-outline" style="width:100%;">Save body info</button>
      <button type="button" class="btn btn-primary" style="width:100%;margin-top:8px;" data-action="calc-targets">Calculate my targets</button>
      <div class="field-hint" style="margin-top:8px;">Uses your latest logged weight (Progress tab). Sets calories, protein, carbs, fat and fiber — you can still fine-tune below.</div>
    </form>

    <div class="section-head"><h2>Daily goals</h2></div>
    <form id="goalsForm" class="card">
      <div class="field-row">
        <div class="field"><label>Calories (kcal)</label><input type="number" name="calorieGoal" value="${g.calorieGoal}" min="0"></div>
        <div class="field"><label>Fiber (g)</label><input type="number" name="fiberGoal" value="${g.fiberGoal}" min="0"></div>
      </div>
      <div class="field-row">
        <div class="field"><label>Protein (g)</label><input type="number" name="proteinGoal" value="${g.proteinGoal}" min="0"></div>
        <div class="field"><label>Carbs (g)</label><input type="number" name="carbGoal" value="${g.carbGoal}" min="0"></div>
        <div class="field"><label>Fat (g)</label><input type="number" name="fatGoal" value="${g.fatGoal}" min="0"></div>
      </div>
      <details class="settings-group"><summary>Micronutrient targets</summary>
        <div class="field-row">
          <div class="field"><label>Sodium limit (mg)</label><input type="number" name="sodiumLimit" value="${g.sodiumLimit}" min="0"></div>
          <div class="field"><label>Potassium (mg)</label><input type="number" name="potassiumGoal" value="${g.potassiumGoal}" min="0"></div>
        </div>
        <div class="field-row">
          <div class="field"><label>Calcium (mg)</label><input type="number" name="calciumGoal" value="${g.calciumGoal}" min="0"></div>
          <div class="field"><label>Iron (mg)</label><input type="number" name="ironGoal" value="${g.ironGoal}" min="0"></div>
        </div>
        <div class="field-row">
          <div class="field"><label>Vitamin A (mcg)</label><input type="number" name="vitAGoal" value="${g.vitAGoal}" min="0"></div>
          <div class="field"><label>Vitamin C (mg)</label><input type="number" name="vitCGoal" value="${g.vitCGoal}" min="0"></div>
        </div>
        <div class="field-hint">The Nutrients tab tracks ~40 more markers (vitamins, minerals, fat subtypes) against fixed general reference values that aren't individually editable here, to keep this form usable.</div>
      </details>
      <button type="submit" class="btn btn-primary" style="margin-top:12px;">Save goals</button>
    </form>

    <div class="section-head"><h2>Weight & units</h2></div>
    <form id="weightSettingsForm" class="card">
      <div class="field"><label>Units</label>
        <div class="chip-row">
          <button type="button" class="chip ${g.unit==='metric'?'active':''}" data-action="set-unit" data-unit="metric">Kilograms</button>
          <button type="button" class="chip ${g.unit==='imperial'?'active':''}" data-action="set-unit" data-unit="imperial">Pounds</button>
        </div>
      </div>
      <div class="field-row">
        <div class="field"><label>Starting weight (${unit})</label><input type="number" step="0.1" name="startWeight" value="${g.startWeightKg!=null? round1(toDisplayWeight(g.startWeightKg)) : ''}"></div>
        <div class="field"><label>Goal weight (${unit})</label><input type="number" step="0.1" name="goalWeight" value="${g.weightGoalKg!=null? round1(toDisplayWeight(g.weightGoalKg)) : ''}"></div>
      </div>
      <button type="submit" class="btn btn-primary">Save</button>
    </form>

    <div class="section-head"><h2>Appearance</h2></div>
    <div class="card"><div class="theme-row" style="padding:0;">${renderThemeButtons()}</div></div>

    <div class="section-head"><h2>Your data</h2></div>
    <div class="card">
      ${!storageOk ? `<div class="disclaimer" style="margin-bottom:12px;">Browser storage isn't available here, so your data won't be saved between visits. Export a backup before you close this tab.</div>` : ''}
      <div class="row gap-8" style="flex-wrap:wrap;">
        <button class="btn btn-outline btn-sm" data-action="export-data">Export backup</button>
        <button class="btn btn-outline btn-sm" data-action="trigger-import">Import backup</button>
        <button class="btn btn-danger btn-sm" data-action="reset-data">Reset all data</button>
      </div>
      <input type="file" id="importFileInput" accept="application/json" style="display:none;">
    </div>
  `;
}

/* ---------- Confirm dialog ---------- */
function openConfirm(message, cb){
  confirmCallback = cb;
  openModalHtml(`
    <div class="modal-head"><h3>Are you sure?</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    <p class="muted" style="font-size:14px;">${escapeHtml(message)}</p>
    <div class="row gap-8" style="margin-top:16px;">
      <button class="btn btn-outline" style="flex:1;" data-action="close-modal">Cancel</button>
      <button class="btn btn-danger" style="flex:1;" data-action="run-confirm">Confirm</button>
    </div>
  `, 'generic');
}

/* ---------- Barcode scanning (floating button -> modal) ---------- */
function openScanModal(){
  lastScanResult = null;
  openModalHtml(scanModalHtml(), 'scan');
}
function scanModalHtml(){
  const supported = 'BarcodeDetector' in window;
  const linked = Object.entries(STATE.barcodeMap);
  let resultBlock = '';
  if(lastScanResult){
    if(lastScanResult.ref){
      const base = resolveRefBase(lastScanResult.ref);
      resultBlock = base ? `<div class="card" style="margin-top:14px;">
        <div class="row between"><strong>${escapeHtml(base.name)}</strong><span class="muted">${escapeHtml(lastScanResult.code)}</span></div>
        <div class="muted" style="font-size:12.5px;margin:4px 0 12px;">${escapeHtml(base.servingLabel)}</div>
        <button class="btn btn-primary btn-sm" data-action="log-scanned">${ICON.plus} Log this food</button>
      </div>` : '';
    } else {
      resultBlock = `<div class="card" style="margin-top:14px;">
        <div class="row between"><strong>New barcode</strong><span class="muted">${escapeHtml(lastScanResult.code)}</span></div>
        <div class="muted" style="font-size:12.5px;margin:4px 0 12px;">Not linked to any food yet.</div>
        <div class="row gap-8">
          <button class="btn btn-outline btn-sm" data-action="link-barcode-existing">Link to existing food</button>
          <button class="btn btn-outline btn-sm" data-action="link-barcode-new">Create custom food</button>
        </div>
      </div>`;
    }
  }
  return `
    <div class="modal-head"><h3>Scan barcode</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    <div class="scan-video-wrap" id="scanVideoWrap" style="${supported?'':'display:none;'}">
      <video id="scanVideo" muted playsinline></video>
      <div class="scan-frame"></div>
    </div>
    ${supported ? `
      <div class="row gap-8" style="margin-top:14px;">
        <button class="btn btn-primary btn-sm" data-action="start-scan" id="scanStartBtn">${ICON.camera} Start camera</button>
        <button class="btn btn-outline btn-sm" data-action="stop-scan" id="scanStopBtn" style="display:none;">Stop</button>
      </div>` : `<div class="empty-state"><div class="big">📷</div>Live camera scanning isn't supported in this browser. Enter the barcode number below instead.</div>`}
    <div id="scanMessage" class="field-hint" style="margin-top:8px;"></div>
    <div class="field" style="margin-top:16px;">
      <label>Or enter the barcode number</label>
      <div class="field-row">
        <input type="text" inputmode="numeric" id="manualBarcode" placeholder="e.g. 8901030871070">
        <button class="btn btn-outline" data-action="lookup-manual-barcode">Look up</button>
      </div>
    </div>
    ${resultBlock}
    <div class="section-head"><h2>Linked barcodes</h2><span class="meta">${linked.length}</span></div>
    ${linked.length ? linked.map(([code,ref])=>{
      const base = resolveRefBase(ref);
      return `<div class="barcode-row"><span class="code">${escapeHtml(code)}</span><span style="flex:1;">${base?escapeHtml(base.name):'(missing food)'}</span>
        <span class="icon-x" data-action="delete-barcode" data-code="${escapeHtml(code)}">${ICON.x}</span></div>`;
    }).join('') : `<div class="muted" style="font-size:13px;">No barcodes linked yet.</div>`}
  `;
}
function renderScanModalBody(){ openModalHtml(scanModalHtml(), 'scan'); }
function showScanMessage(msg){ const el = document.getElementById('scanMessage'); if(el) el.textContent = msg; }
async function startScan(){
  const video = document.getElementById('scanVideo');
  if(!video) return;
  if(!('BarcodeDetector' in window)){ showScanMessage("Live camera scanning isn't supported in this browser — use manual entry below."); return; }
  try{
    let formats;
    try{ formats = await window.BarcodeDetector.getSupportedFormats(); }catch(e){ formats = ['ean_13','ean_8','upc_a','upc_e','code_128']; }
    scanDetector = new window.BarcodeDetector({formats});
    scanStream = await navigator.mediaDevices.getUserMedia({video:{facingMode:'environment'}});
    video.srcObject = scanStream;
    await video.play();
    scanning = true;
    const startBtn = document.getElementById('scanStartBtn'), stopBtn = document.getElementById('scanStopBtn');
    if(startBtn) startBtn.style.display = 'none';
    if(stopBtn) stopBtn.style.display = '';
    showScanMessage('Point your camera at a barcode.');
    scanLoop();
  }catch(err){ showScanMessage("Camera access isn't available here — use manual entry below."); }
}
function scanLoop(){
  if(!scanning) return;
  const video = document.getElementById('scanVideo');
  if(!video){ scanning=false; return; }
  scanDetector.detect(video).then(codes=>{
    if(codes && codes.length){ const code = codes[0].rawValue; handleBarcode(code); }
    else if(scanning){ requestAnimationFrame(scanLoop); }
  }).catch(()=>{ if(scanning) requestAnimationFrame(scanLoop); });
}
function stopScan(){
  scanning = false;
  if(scanStream){ scanStream.getTracks().forEach(t=>t.stop()); scanStream = null; }
  const startBtn = document.getElementById('scanStartBtn'), stopBtn = document.getElementById('scanStopBtn');
  if(startBtn) startBtn.style.display = '';
  if(stopBtn) stopBtn.style.display = 'none';
}
function handleBarcode(code){
  code = (code||'').toString().trim();
  if(!code) return;
  stopScan();
  const mapping = STATE.barcodeMap[code];
  lastScanResult = {code, ref: mapping || null};
  renderScanModalBody();
}

/* ---------- Export / Import ---------- */
async function exportData(){
  const json = JSON.stringify(STATE, null, 2);
  const filename = 'tiffin-backup-'+todayKey()+'.json';
  try{
    if(window.claude && window.claude.use){
      const downloads = await window.claude.use('downloads');
      if(downloads){
        try{ await downloads.save({filename, data: json}); toast('Backup saved.'); return; }
        catch(err){ if(err && err.code === 'declined'){ return; } }
      }
    }
  }catch(e){}
  openModalHtml(`
    <div class="modal-head"><h3>Export backup</h3><button class="close-btn" data-action="close-modal">${ICON.x}</button></div>
    <p class="field-hint">Copy this text and save it somewhere safe.</p>
    <textarea readonly style="width:100%;height:220px;font-size:11px;padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--surface);">${escapeHtml(json)}</textarea>
    <button class="btn btn-primary" style="width:100%;margin-top:12px;" data-action="copy-export-text">Copy to clipboard</button>
  `, 'generic');
}
function importFromFile(file){
  const reader = new FileReader();
  reader.onload = ()=>{
    try{
      const parsed = JSON.parse(reader.result);
      const s = defaultState();
      s.goals = mergeKnownFields(DEFAULT_GOALS, parsed.goals);
      s.profile = mergeKnownFields(defaultProfile(), parsed.profile);
      s.diary = parsed.diary || {};
      s.weightLog = Array.isArray(parsed.weightLog) ? parsed.weightLog : [];
      s.customFoods = Array.isArray(parsed.customFoods) ? parsed.customFoods : [];
      s.customMeals = Array.isArray(parsed.customMeals) ? parsed.customMeals : [];
      s.barcodeMap = parsed.barcodeMap || {};
      s.mealSlots = Array.isArray(parsed.mealSlots) && parsed.mealSlots.length ? parsed.mealSlots : defaultMealSlots();
      STATE = s;
      saveState(); applyTheme(); renderApp();
      toast('Backup imported.');
    }catch(e){ toast("That file couldn't be read as a Tiffin backup."); }
  };
  reader.readAsText(file);
}

/* ---------- Theme ---------- */
function applyTheme(){
  const t = STATE.goals.theme || 'system';
  if(t === 'system') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', t);
}

/* ---------- Event delegation ---------- */
function onClick(e){
  const t = e.target.closest('[data-action]');
  if(!t) return;
  const action = t.dataset.action;

  if(action === 'nav'){ currentView = t.dataset.view; renderApp(); return; }
  if(action === 'date-prev'){ currentDate = addDaysKey(currentDate,-1); renderView(); return; }
  if(action === 'date-next'){ currentDate = addDaysKey(currentDate,1); renderView(); return; }
  if(action === 'set-theme'){ STATE.goals.theme = t.dataset.theme; saveState(); applyTheme(); renderShell(); if(currentView==='progress') renderWeightChartNow(); return; }
  if(action === 'set-unit'){ STATE.goals.unit = t.dataset.unit; saveState(); renderView(); return; }
  if(action === 'open-energy-modal'){ openEnergyModal(); return; }
  if(action === 'goto-profile-from-modal'){ closeModal(); currentView='profile'; renderApp(); return; }

  /* Picker: add-one-at-a-time list step */
  if(action === 'open-picker'){ openPicker({meal:t.dataset.meal}); return; }
  if(action === 'close-modal'){ closeModal(); return; }
  if(action === 'picker-filter-cat'){ picker.cat = t.dataset.cat; renderPickerModal(); return; }
  if(action === 'foods-filter-cat'){ foodsFilter.cat = t.dataset.cat; renderView(); return; }
  if(action === 'select-food'){
    const ref = {type:t.dataset.refType, id:t.dataset.refId};
    const base = resolveRefBase(ref);
    if(!base) return;
    picker.activeRef = ref;
    picker.activeUnit = 'medium';
    picker.activeAmount = 1;
    picker.step = 'serving';
    renderPickerModal();
    return;
  }
  if(action === 'pick-link'){
    const ref = {type:t.dataset.refType, id:t.dataset.refId};
    STATE.barcodeMap[picker.pendingBarcode] = ref;
    saveState();
    lastScanResult = {code:picker.pendingBarcode, ref};
    toast('Barcode linked.');
    renderScanModalBody();
    return;
  }
  if(action === 'quick-add'){
    const ref = {type:t.dataset.refType, id:t.dataset.refId};
    const base = resolveRefBase(ref);
    if(!base) return;
    openPicker({step:'serving', activeRef:ref, activeUnit:'medium', activeAmount:1, meal:null, singleMode:true});
    return;
  }
  if(action === 'set-serving-unit'){
    const base = resolveRefBase(picker.activeRef);
    const oldGrams = computeGrams(base, picker.activeUnit, picker.activeAmount);
    picker.activeUnit = t.dataset.unit;
    picker.activeAmount = defaultAmountForUnit(base, picker.activeUnit, oldGrams);
    renderPickerModal();
    return;
  }
  if(action === 'serving-cancel'){ picker.activeRef = null; picker.step = 'list'; renderPickerModal(); return; }
  if(action === 'add-to-cart'){
    const base = resolveRefBase(picker.activeRef);
    const grams = computeGrams(base, picker.activeUnit, picker.activeAmount);
    picker.cart.push({ref:picker.activeRef, unit:picker.activeUnit, amount:picker.activeAmount, grams});
    picker.activeRef = null;
    picker.step = 'list';
    renderPickerModal();
    toast('Added to list.');
    return;
  }
  if(action === 'cart-remove'){ picker.cart.splice(parseInt(t.dataset.index,10),1); renderPickerModal(); return; }
  if(action === 'picker-finish'){
    const meal = picker.meal || STATE.mealSlots[0].id;
    const day = getDay(picker.dateKey);
    const addedCount = picker.cart.length;
    picker.cart.forEach(item=>{
      const base = resolveRefBase(item.ref);
      const qty = base && base.servingGrams>0 ? item.grams/base.servingGrams : 1;
      day[meal].push({ref:item.ref, qty});
    });
    saveState(); closeModal();
    toast('Added '+addedCount+' food'+(addedCount>1?'s':'')+' to '+mealName(meal)+'.');
    renderView();
    return;
  }
  if(action === 'commit-single'){
    const base = resolveRefBase(picker.activeRef);
    const grams = computeGrams(base, picker.activeUnit, picker.activeAmount);
    const qty = base && base.servingGrams>0 ? grams/base.servingGrams : 1;
    const sel = document.getElementById('pickerMealSelect');
    const meal = picker.meal || (sel ? sel.value : STATE.mealSlots[0].id);
    const day = getDay(picker.dateKey);
    const wasEdit = picker.editMeal != null && picker.editIndex != null;
    if(wasEdit){ day[picker.editMeal].splice(picker.editIndex,1); }
    day[meal].push({ref:picker.activeRef, qty});
    saveState(); closeModal();
    toast(wasEdit ? 'Saved.' : 'Added to '+mealName(meal)+'.');
    renderView();
    return;
  }
  if(action === 'edit-entry'){
    const meal = t.dataset.meal, idx = parseInt(t.dataset.index,10);
    const entry = getDay(currentDate)[meal][idx];
    const base = resolveRefBase(entry.ref);
    const grams = base ? entry.qty*base.servingGrams : 100;
    openPicker({step:'serving', meal, dateKey:currentDate, activeRef:entry.ref, activeUnit:'grams', activeAmount:Math.round(grams), editMeal:meal, editIndex:idx});
    return;
  }
  if(action === 'delete-entry'){
    e.stopPropagation();
    const meal = t.dataset.meal, idx = parseInt(t.dataset.index,10);
    getDay(currentDate)[meal].splice(idx,1);
    saveState(); renderView();
    return;
  }

  if(action === 'open-custom-food'){ pendingCustomFoodBarcode = picker && picker.pendingBarcode ? picker.pendingBarcode : pendingCustomFoodBarcode; openCustomFoodForm(); return; }
  if(action === 'open-custom-meal'){ openCustomMealForm(); return; }
  if(action === 'add-meal-item'){ mealBuilder.items.push({ref:{type:t.dataset.refType, id:t.dataset.refId}, qty:1}); mealBuilder.query=''; renderMealBuilderModal(); return; }
  if(action === 'remove-meal-item'){ mealBuilder.items.splice(parseInt(t.dataset.index,10),1); renderMealBuilderModal(); return; }
  if(action === 'save-custom-meal'){
    const nameInput = document.getElementById('mealBuilderName');
    const name = (nameInput.value||'').trim();
    if(!name){ toast('Give your meal a name.'); return; }
    if(!mealBuilder.items.length){ toast('Add at least one ingredient.'); return; }
    STATE.customMeals.push({id:'meal-'+uid(), name, items: mealBuilder.items.map(i=>({ref:i.ref, qty:i.qty}))});
    saveState(); closeModal(); toast('Custom meal saved.'); renderView();
    return;
  }
  if(action === 'delete-custom-food'){
    e.stopPropagation();
    const id = t.dataset.id;
    openConfirm('Delete this custom food? This also removes it from your diary and any custom meals that use it, and cannot be undone.', ()=>{
      STATE.customFoods = STATE.customFoods.filter(f=>f.id!==id);
      purgeFoodRef({type:'custom', id});
      saveState(); renderView(); toast('Custom food deleted.');
    });
    return;
  }
  if(action === 'delete-custom-meal'){
    e.stopPropagation();
    const id = t.dataset.id;
    openConfirm('Delete this custom meal? This also removes it from your diary, and cannot be undone.', ()=>{
      STATE.customMeals = STATE.customMeals.filter(m=>m.id!==id);
      purgeFoodRef({type:'meal', id});
      saveState(); renderView(); toast('Custom meal deleted.');
    });
    return;
  }

  /* Meal slot management */
  if(action === 'open-meal-slots'){ openMealSlotsModal(); return; }
  if(action === 'slot-cycle-emoji'){
    const s = mealSlot(t.dataset.id);
    if(s){ const i = EMOJI_PALETTE.indexOf(s.emoji); s.emoji = EMOJI_PALETTE[(i+1) % EMOJI_PALETTE.length]; saveState(); renderMealSlotsModal(); }
    return;
  }
  if(action === 'slot-move-up'){
    const i = parseInt(t.dataset.index,10);
    if(i>0){ const arr = STATE.mealSlots; [arr[i-1],arr[i]] = [arr[i],arr[i-1]]; saveState(); renderMealSlotsModal(); }
    return;
  }
  if(action === 'slot-move-down'){
    const i = parseInt(t.dataset.index,10);
    const arr = STATE.mealSlots;
    if(i<arr.length-1){ [arr[i+1],arr[i]] = [arr[i],arr[i+1]]; saveState(); renderMealSlotsModal(); }
    return;
  }
  if(action === 'slot-delete'){
    const i = parseInt(t.dataset.index,10);
    const slot = STATE.mealSlots[i];
    if(STATE.mealSlots.length <= 1){ toast('You need at least one meal.'); return; }
    openConfirm(`Delete "${slot.name}"? Any foods already logged under it will be removed too.`, ()=>{
      STATE.mealSlots.splice(i,1);
      Object.keys(STATE.diary).forEach(dateKey=>{ delete STATE.diary[dateKey][slot.id]; });
      saveState(); renderMealSlotsModal(); renderShell();
      toast('Meal deleted.');
    });
    return;
  }
  if(action === 'slot-add'){
    const n = STATE.mealSlots.length + 1;
    STATE.mealSlots.push({id:'meal-'+uid(), name:'Meal '+n, emoji: EMOJI_PALETTE[STATE.mealSlots.length % EMOJI_PALETTE.length]});
    saveState(); renderMealSlotsModal();
    return;
  }

  /* Water */
  if(action === 'set-water-glass'){
    const day = getDay(currentDate);
    const i = parseInt(t.dataset.index,10);
    const glassSize = 250;
    const filled = Math.round((day.water||0)/glassSize);
    day.water = (i < filled) ? i*glassSize : (i+1)*glassSize;
    saveState(); renderView();
    return;
  }
  if(action === 'add-water'){
    const day = getDay(currentDate);
    day.water = (day.water||0) + parseInt(t.dataset.ml,10);
    saveState(); renderView();
    return;
  }
  if(action === 'add-water-custom'){
    const input = document.getElementById('waterCustomInput');
    const v = parseInt(input && input.value, 10);
    if(!isNaN(v) && v>0){ const day = getDay(currentDate); day.water = (day.water||0) + v; saveState(); renderView(); }
    return;
  }
  if(action === 'reset-water'){ getDay(currentDate).water = 0; saveState(); renderView(); return; }
  if(action === 'delete-workout'){
    getDay(currentDate).workouts.splice(parseInt(t.dataset.index,10),1);
    saveState(); renderView();
    return;
  }

  /* Scan */
  if(action === 'open-scan-modal'){ openScanModal(); return; }
  if(action === 'start-scan'){ startScan(); return; }
  if(action === 'stop-scan'){ stopScan(); showScanMessage(''); return; }
  if(action === 'lookup-manual-barcode'){
    const input = document.getElementById('manualBarcode');
    if(input && input.value.trim()) handleBarcode(input.value);
    return;
  }
  if(action === 'log-scanned'){
    const ref = lastScanResult.ref;
    closeModal();
    openPicker({step:'serving', activeRef:ref, activeUnit:'medium', activeAmount:1, meal:null, singleMode:true});
    return;
  }
  if(action === 'link-barcode-existing'){ const bc = lastScanResult.code; closeModal(); openPicker({step:'list', linkOnly:true, pendingBarcode:bc}); return; }
  if(action === 'link-barcode-new'){ pendingCustomFoodBarcode = lastScanResult.code; closeModal(); openCustomFoodForm(); return; }
  if(action === 'delete-barcode'){
    openConfirm('Remove this barcode link?', ()=>{ delete STATE.barcodeMap[t.dataset.code]; saveState(); toast('Barcode link removed.'); });
    return;
  }

  if(action === 'delete-weight'){
    openConfirm('Delete this weigh-in?', ()=>{ STATE.weightLog.splice(parseInt(t.dataset.index,10),1); saveState(); renderView(); });
    return;
  }

  /* Profile: body & goal chips */
  if(action === 'set-sex'){ STATE.profile.sex = t.dataset.sex; saveState(); renderView(); return; }
  if(action === 'set-goal-type'){ STATE.profile.goalType = t.dataset.goal; saveState(); renderView(); return; }
  if(action === 'set-height-unit'){ STATE.profile.heightUnit = t.dataset.unit; renderView(); return; }
  if(action === 'set-weekly-rate'){ STATE.profile.weeklyRateKg = parseFloat(t.dataset.rate); saveState(); renderView(); return; }
  if(action === 'calc-targets'){ calculateTargetsFromProfile(); return; }

  if(action === 'export-data'){ exportData(); return; }
  if(action === 'copy-export-text'){
    const ta = document.querySelector('#modalContent textarea');
    if(ta){ ta.select(); navigator.clipboard && navigator.clipboard.writeText(ta.value).then(()=>toast('Copied.')).catch(()=>toast('Select the text and copy manually.')); }
    return;
  }
  if(action === 'trigger-import'){ document.getElementById('importFileInput').click(); return; }
  if(action === 'reset-data'){
    openConfirm('Reset all data? This deletes your diary, foods, weight log and settings, and cannot be undone.', ()=>{
      STATE = defaultState(); saveState(); applyTheme(); renderApp(); toast('All data reset.');
    });
    return;
  }
  if(action === 'run-confirm'){
    const cb = confirmCallback; confirmCallback = null;
    closeModal();
    if(cb) cb();
    return;
  }
}

function onInput(e){
  const el = e.target;
  if(el.id === 'foodsSearch'){ foodsFilter.query = el.value; document.getElementById('foodsList').innerHTML = foodRowsHtml(filterFoods(allBrowsable(), foodsFilter.query, foodsFilter.cat),{mode:'quickadd', allowDelete:true}); return; }
  if(el.id === 'pickerSearch'){
    picker.query = el.value;
    const list = filterFoods(allBrowsable(), picker.query, picker.cat);
    document.getElementById('pickerList').innerHTML = foodRowsHtml(list, {mode:picker.linkOnly?'link':'pick'});
    return;
  }
  if(el.id === 'mealBuilderSearch'){ mealBuilder.query = el.value; renderMealBuilderModal(); focusEnd('mealBuilderSearch'); return; }
  if(el.id === 'mealBuilderName'){ mealBuilder.name = el.value; return; }
  if(el.hasAttribute && el.hasAttribute('data-slot-name')){
    const s = mealSlot(el.getAttribute('data-slot-name'));
    if(s){ s.name = el.value; saveState(); }
    return;
  }
  if(el.id === 'servingAmount'){
    const v = parseFloat(el.value);
    if(!isNaN(v) && v>0){
      picker.activeAmount = v;
      const base = resolveRefBase(picker.activeRef);
      if(base){
        const grams = computeGrams(base, picker.activeUnit, v);
        const qty = base.servingGrams>0 ? grams/base.servingGrams : 1;
        const n = scaleNutrients(base.nutrients, qty);
        const setText = (id,val)=>{ const e=document.getElementById(id); if(e) e.textContent=val; };
        setText('servingKcal', Math.round(n.kcal));
        setText('servingProtein', round1(n.protein)+'g');
        setText('servingCarbs', round1(n.carbs)+'g');
        setText('servingFat', round1(n.fat)+'g');
      }
    }
    return;
  }
}
function focusEnd(id){ const el = document.getElementById(id); if(el){ el.focus(); const v = el.value; el.value=''; el.value=v; } }

function onChange(e){
  const el = e.target;
  if(el.id === 'importFileInput' && el.files && el.files[0]){ importFromFile(el.files[0]); el.value=''; return; }
}

function onSubmit(e){
  const form = e.target;
  if(form.id === 'customFoodForm'){ e.preventDefault(); handleCustomFoodSubmit(form); return; }
  if(form.id === 'profileForm'){
    e.preventDefault();
    const fd = new FormData(form);
    STATE.profile.name = (fd.get('name')||'').toString().trim();
    saveState(); toast('Profile saved.'); renderShell();
    return;
  }
  if(form.id === 'bodyForm'){
    e.preventDefault();
    const fd = new FormData(form);
    const age = parseInt(fd.get('age'),10); STATE.profile.age = isNaN(age) ? null : age;
    if((STATE.profile.heightUnit||'cm') === 'ft'){
      const ft = parseFloat(fd.get('heightFt'))||0, inch = parseFloat(fd.get('heightIn'))||0;
      STATE.profile.heightCm = (ft>0 || inch>0) ? Math.round((ft*12+inch)*2.54) : null;
    } else {
      const h = parseFloat(fd.get('heightCm')); STATE.profile.heightCm = isNaN(h) ? null : h;
    }
    STATE.profile.activityLevel = fd.get('activityLevel') || 'moderate';
    const wg = parseFloat(fd.get('waterGoalMl')); if(!isNaN(wg)) STATE.goals.waterGoalMl = wg;
    saveState(); toast('Saved.'); renderView();
    return;
  }
  if(form.id === 'goalsForm'){
    e.preventDefault();
    const fd = new FormData(form);
    ['calorieGoal','proteinGoal','carbGoal','fatGoal','fiberGoal','sodiumLimit','potassiumGoal','calciumGoal','ironGoal','vitAGoal','vitCGoal'].forEach(k=>{
      const v = parseFloat(fd.get(k)); if(!isNaN(v)) STATE.goals[k] = v;
    });
    saveState(); toast('Goals saved.'); renderView();
    return;
  }
  if(form.id === 'weightSettingsForm'){
    e.preventDefault();
    const fd = new FormData(form);
    const sw = parseFloat(fd.get('startWeight')), gw = parseFloat(fd.get('goalWeight'));
    STATE.goals.startWeightKg = isNaN(sw) ? null : fromDisplayWeight(sw);
    STATE.goals.weightGoalKg = isNaN(gw) ? null : fromDisplayWeight(gw);
    saveState(); toast('Saved.'); renderView();
    return;
  }
  if(form.id === 'weightForm'){
    e.preventDefault();
    const fd = new FormData(form);
    const date = fd.get('date'); const w = parseFloat(fd.get('weight'));
    if(!date || isNaN(w) || w<=0){ toast('Enter a valid weight.'); return; }
    const kg = fromDisplayWeight(w);
    const existingIdx = STATE.weightLog.findIndex(x=>x.date===date);
    if(existingIdx>=0) STATE.weightLog[existingIdx].kg = kg;
    else STATE.weightLog.push({date, kg});
    saveState(); toast('Weight logged.'); renderView();
    return;
  }
  if(form.id === 'workoutForm'){
    e.preventDefault();
    const fd = new FormData(form);
    const name = (fd.get('name')||'').toString().trim();
    if(!name) return;
    const duration = parseInt(fd.get('duration'),10);
    getDay(currentDate).workouts.push({name, duration: isNaN(duration)?null:duration});
    saveState(); toast('Workout logged.'); renderView();
    return;
  }
}

/* ---------- Init ---------- */
let inited = false;
function init(){
  if(inited) return; inited = true;
  applyTheme();
  document.addEventListener('click', onClick);
  document.addEventListener('input', onInput);
  document.addEventListener('change', onChange);
  document.addEventListener('submit', onSubmit);
  document.getElementById('modalOverlay').addEventListener('click', function(e){ if(e.target.id === 'modalOverlay') closeModal(); });
  if(!storageOk){ setTimeout(()=> toast("Your data won't be saved between visits — browser storage is unavailable here."), 400); }
  renderApp();
}
document.addEventListener('DOMContentLoaded', init);
if(document.readyState !== 'loading') init();

})();
