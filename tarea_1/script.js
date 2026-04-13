function isEmail(v){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);}
function isURL(v){return /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- ./?%&=]*)?$/.test(v);}

function validateRegister(){
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let type = document.getElementById("type").value;

  if(!name || !email || !type){ alert("Required fields missing"); return false;}
  if(!isEmail(email)){ alert("Invalid email"); return false;}
  alert("Valid!");
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
    {name:"Ana", type:"student_undergrad", email:"z@mail.com"},
    {name:"Luis", type:"faculty", email:"x@mail.com"},
    {name:"Eva", type:"staff", email:"y@mail.com"}
  ];

  let filter = document.getElementById("filter").value;
  let sort = document.getElementById("sort").value;

  let filtered = filter ? data.filter(d=>d.type===filter) : data;

  filtered.sort((a,b)=> a[sort].localeCompare(b[sort]));

  let tbody = document.getElementById("tbody");
  tbody.innerHTML="";
  filtered.forEach(d=>{
    tbody.innerHTML += `<tr><td>${d.name}</td><td>${d.type}</td><td>${d.email}</td></tr>`;
  });
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
  let name = document.getElementById("mname").value;
  let file = document.getElementById("file").files.length;
  let link = document.getElementById("link").value;

  if(!name || file === 0 || !link){
    alert("Required fields missing");
    return false;
  }

  if(schedules.length === 0){
    alert("At least one schedule is required");
    return false;
  }

  if(!isURL(link)){
    alert("Invalid URL");
    return false;
  }

  alert("Valid!");
  return false;
}