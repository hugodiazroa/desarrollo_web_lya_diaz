function isEmail(v){return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);}
function isURL(v){return /^(https?:\/\/)?([\w-]+\.)+[\w-]+(\/[\w- ./?%&=]*)?$/.test(v);}

function validateRegister(){
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let type = document.getElementById("type").value;
  let extra = document.getElementById("extra").value;

  if(!name || !email || !type){ alert("Required fields missing"); return false;}
  if(!isEmail(email)){ alert("Invalid email"); return false;}
  if(!extra){ alert("Role-specific field required"); return false;}
  alert("Valid!");
  return false;
}

function validateActivity(){
  let name = document.getElementById("mname").value;
  let file = document.getElementById("file").files.length;
  let link = document.getElementById("link").value;

  if(!name || file === 0 || !link){ alert("Required fields missing"); return false;}
  if(!isURL(link)){ alert("Invalid URL"); return false;}
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
    {name:"Ana", type:"student_undergrad", email:"a@mail.com"},
    {name:"Luis", type:"faculty", email:"l@mail.com"},
    {name:"Eva", type:"staff", email:"e@mail.com"}
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