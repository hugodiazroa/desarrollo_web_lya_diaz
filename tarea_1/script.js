function isEmail(v){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);}
function isURL(v){return /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- ./?%&=]*)?$/.test(v);}

function validateRegister(){
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let type = document.getElementById("type").value;

  if(!name || !email || !type){ alert("Required fields missing"); return false;}
  if(!isEmail(email)){ alert("Invalid email"); return false;}

  setUser(name);
  renderUser();

  alert("Registered!");
  return false;
}

function updateExtra(){
  let type = document.getElementById("type").value;
  let label = document.getElementById("extraLabel");
  if(type.includes("student")) label.innerText="Program *";
  else label.innerText="Department *";
}

function loadMembers(){
  let data = [
    {
      name:"Ana",
      type:"student_undergrad",
      email:"x@mail.com",
      activities:[
        {name:"Programar perros", category:"Tech", link:"https://example.com/a1"},
        {name:"Pasear perros", category:"Social", link:"https://example.com/a2"}
      ]
    },
    {
      name:"Luis",
      type:"faculty",
      email:"y@mail.com",
      activities:[]
    },
    {
      name:"Eva",
      type:"staff",
      email:"z@mail.com",
      activities:[
        {name:"Pintar gatos", category:"Artistic", link:"https://example.com/e1"}
      ]
    },
    {
      name:"Carlos",
      type:"student_grad",
      email:"a@mail.com",
      activities:[
        {name:"Maraton", category:"Athletic", link:"https://example.com/c1"},
        {name:"Torneo de ajedrez", category:"Recreational", link:"https://example.com/c2"},
        {name:"Congreso sobre programacion", category:"Tech", link:"https://example.com/c3"}
      ]
    },
    {
      name:"María",
      type:"student_undergrad",
      email:"v@mail.com",
      activities:[]
    },
    {
      name:"Jorge",
      type:"faculty",
      email:"r@mail.com",
      activities:[
        {name:"", category:"Social", link:"https://example.com/j1"}
      ]
    }
  ];

  let filter = document.getElementById("filter").value;
  let sort = document.getElementById("sort").value;

  let filtered = filter ? data.filter(d=>d.type===filter) : data;
  filtered.sort((a,b)=> a[sort].localeCompare(b[sort]));

  let tbody = document.getElementById("tbody");
  tbody.innerHTML="";

  filtered.forEach((d, index)=>{
    tbody.innerHTML += `
      <tr onclick="toggleActivities(${index})" style="cursor:pointer;">
        <td>${d.name}</td>
        <td>${d.type}</td>
        <td>${d.email}</td>
      </tr>
      <tr id="activities-${index}" style="display:none;">
        <td colspan="3">${renderActivities(d.activities)}</td>
      </tr>
    `;
  });

  window._members = filtered; // store globally for access
}

function renderActivities(activities){
  if(!activities || activities.length === 0){
    return "<em>No activities</em>";
  }

  return activities.map(a=>{
    return `
      <strong>${a.name}</strong> (${a.category}) - 
      <a href="${a.link}" target="_blank">${a.link}</a>
    `;
  }).join("<br>");
}

function toggleActivities(index){
  let row = document.getElementById(`activities-${index}`);
  row.style.display = row.style.display === "none" ? "table-row" : "none";
}

let schedules = [];

function addSchedule(){
  let day = document.getElementById("day").value;
  let hour = document.getElementById("hour").value;
  let minute = document.getElementById("minute").value;
  let duration = document.getElementById("duration").value;

  if(!day || !hour || !minute || !duration){
    alert("All schedule fields required");
    return;
  }

  if(duration <= 0 || duration > 240){
    alert("Duration must be 1–240 minutes");
    return;
  }

  let entry = `${day} ${hour}:${minute} (${duration} min)`;
  schedules.push(entry);

  let list = document.getElementById("scheduleList");
  list.innerHTML += `<li>${entry}</li>`;
}

function validateActivity(){
  let name = localStorage.getItem("activeUser");
  let activityName = document.getElementById("activityName").value;
  let inputs = document.querySelectorAll("#fileContainer input[type='file']");
  let files = Array.from(inputs).flatMap(i => Array.from(i.files));
  let link = document.getElementById("link").value;

  const MAX_SIZE = 100 * 1024 * 1024; // 100MB
  const MAX_FILES = 8;

  if(!name || !activityName || files.length === 0 || !link){
    alert("Required fields missing");
    return false;
  }

  if(files.length > MAX_FILES){
    alert("You can upload at most 8 files");
    return false;
  }

  if(schedules.length === 0){
    alert("At least one schedule is required");
    return false;
  }

  for(let file of files){
    const isValidType = file.type.startsWith("image/") || file.type.startsWith("video/");
    if(!isValidType){
      alert("Only image or video files are allowed");
      return false;
    }

    if(file.size > MAX_SIZE){
      alert("Each file must be less than 100 MB");
      return false;
    }
  }

  if(!isURL(link)){
    alert("Invalid URL");
    return false;
  }

  alert("Valid!");
  return false;
}

function handleFileSelection(){
  const input = document.getElementById("file");
  const info = document.getElementById("fileInfo");
  const MAX_FILES = 8;

  if(!input || !info) return;

  const files = input.files;

  if(files.length > MAX_FILES){
    alert("You can upload at most 8 files");
    input.value = "";
    info.textContent = "0 / 8 files selected";
    return;
  }

  info.textContent = `${files.length} / 8 files selected`;
}

function handleSingleFile(input){
  const container = document.getElementById("fileContainer");
  const info = document.getElementById("fileInfo");
  const MAX_FILES = 8;

  const inputs = container.querySelectorAll("input[type='file']");
  const filledInputs = Array.from(inputs).filter(i => i.files.length > 0);

  // update counter
  info.textContent = `${filledInputs.length} / ${MAX_FILES} files selected`;

  // stop if max reached
  if(filledInputs.length >= MAX_FILES) return;

  // only add new input if current one has a file and is the last input
  if(input.files.length > 0 && input === inputs[inputs.length - 1]){
    const newInput = document.createElement("input");
    newInput.type = "file";
    newInput.accept = "image/*,video/*";
    newInput.onchange = function(){ handleSingleFile(this); };

    container.appendChild(newInput);
  }
}

function setUser(name){
  localStorage.setItem("activeUser", name);
}

function logout(){
  localStorage.removeItem("activeUser");
  location.reload();
}

function renderUser(){
  const container = document.getElementById("userStatus");
  const user = localStorage.getItem("activeUser");

  if(!container) return;

  if(user){
    container.innerHTML = `
      <div>${user}</div>
      <div><a href="#" onclick="logout()">Log out</a></div>
    `;
  } else {
    container.innerHTML = `<div>You are not logged in</div>`;
  }
}

function toggleActivityAccess(){
  const user = localStorage.getItem("activeUser");
  const form = document.getElementById("activityForm");
  const msg = document.getElementById("activityMessage");

  if(!form || !msg) return;

  if(user){
    form.style.display = "block";
    msg.style.display = "none";
  } else {
    form.style.display = "none";
    msg.style.display = "block";
  }
}

function fillActiveUser(){
  const user = localStorage.getItem("activeUser");
  const el = document.getElementById("activeUserName");

  if(el && user){
    el.textContent = user;
  }
}

window.addEventListener("load", () => {
  renderUser();
  toggleActivityAccess();
  fillActiveUser();
});