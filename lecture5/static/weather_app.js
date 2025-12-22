console.log('main.js loaded');
fetch(AREA_URL)
  .then(res => {
    console.log('status:', res.status);
    return res.json();
  })
  .then(data => {
    console.log('area data:', data);
  })
  .catch(err => console.error(err));
  
const AREA_URL = 'http://www.jma.go.jp/bosai/common/const/area.json';
const FORECAST_URL = 'https://www.jma.go.jp/bosai/forecast/data/forecast/';

const selectEl = document.getElementById('area-select');
const forecastEl = document.getElementById('forecast');

async function fetchAreaList() {
  try {
    const res = await fetch(AREA_URL);
    if (!res.ok) throw new Error(res.statusText);
    const data = await res.json();
    // data は大項目（都道府県ごとの配列）を持つ
    Object.keys(data).forEach(groupName => {
      const optgroup = document.createElement('optgroup');
      optgroup.label = groupName;
      data[groupName].forEach(area => {
        const opt = document.createElement('option');
        opt.value = area.code;       // ex. "016000"
        opt.textContent = area.name; // ex. "北海道"
        optgroup.appendChild(opt);
      });
      selectEl.appendChild(optgroup);
    });
  } catch (err) {
    console.error('地域一覧の取得失敗:', err);
    selectEl.innerHTML = '<option>地域一覧の取得に失敗しました</option>';
  }
}

async function fetchForecast(code) {
  forecastEl.textContent = '読み込み中…';
  try {
    const res = await fetch(`${FORECAST_URL}${code}.json`);
    if (!res.ok) throw new Error(res.statusText);
    const json = await res.json();
    renderForecast(json);
  } catch (err) {
    console.error('天気予報の取得失敗:', err);
    forecastEl.textContent = '天気予報の取得に失敗しました';
  }
}

function renderForecast(data) {
  // data[0] が「主に今日～明日の概況」、data[1] が「地域ごとの予報」など
  const items = data[1]?.timeSeries?.[0]?.areas || [];
  // シンプルに「日付・天気・最高/最低気温」を表示
  forecastEl.innerHTML = '';
  items.forEach(area => {
    const dayDiv = document.createElement('div');
    dayDiv.className = 'day';
    dayDiv.innerHTML = `
      <strong>${area.area.name}</strong><br>
      天気: ${area.weathers.join(' / ')}<br>
      最高: ${area.temperature.max?.celsius ?? '―'}℃　最低: ${area.temperature.min?.celsius ?? '―'}℃
    `;
    forecastEl.appendChild(dayDiv);
  });
}

// イベント
selectEl.addEventListener('change', () => {
  const code = selectEl.value;
  if (code) fetchForecast(code);
});

// 初期化
fetchAreaList();