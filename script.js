let body = document.body;
let toggle = document.querySelector('.toggle');
let navBar = document.querySelector("nav");
let name = document.querySelector('.name');
let favIcon = document.querySelector(".favicon");
let infoContainer = document.querySelector(".info_container");
let quoteContainer = document.querySelector(".quote_container")
let cards = document.querySelectorAll(".card");
let subLinks = document.querySelectorAll(".web_link p");
let subNav = document.querySelector(".sub_nav");
let quotation = document.querySelector('.quotation');
let author = document.querySelector('.author');
let darkIcon = document.getElementById('dark_icon');
let lightIcon = document.getElementById('light_icon');
let darkToggle = document.getElementById("dark_toggle");
let lightToggle = document.getElementById("light_toggle");
let storedTheme = localStorage.getItem('theme');
let isSystemModeDark = window.matchMedia('(prefers-color-scheme:dark)').matches;

let rotation=0;
let setTheme = (theme) => {
   if (theme === 'dark'){
       body.classList.remove("light")
       body.classList.add("dark")
       darkIcon.classList.remove('hide');
       lightIcon.classList.add('hide');
       darkToggle.classList.remove('hide');
       lightToggle.classList.add("hide");
    } else{
        body.classList.remove("dark")
        body.classList.add("light")
        darkIcon.classList.add('hide');
        lightIcon.classList.remove('hide');
        darkToggle.classList.add('hide');
        lightToggle.classList.remove("hide");
    }
    rotation += 360;
    toggle.style.transform = `rotate(${rotation}deg)`;
}

if (storedTheme){
    setTheme(storedTheme);
} else if(isSystemModeDark){
    setTheme('dark');
} else {
    setTheme('light');
}

favIcon.addEventListener('click', () => {
    let newTheme=body.classList.contains('dark') ? 'light' : 'dark' ;
    setTheme(newTheme);
    localStorage.setItem('theme' , newTheme) ;
});

toggle.addEventListener('click' , () => {
    let newTheme=body.classList.contains('dark') ? 'light' : 'dark' ;
    setTheme(newTheme);
    localStorage.setItem('theme' , newTheme);
});

let object;

let callBack= (entries) => {
    if (!(entries[0].isIntersecting)){
        navBar.style.transform='translateY(0%)';
        }else{
        navBar.style.transform='translateY(-100%)'}
}

let obj= new IntersectionObserver(callBack,object);
obj.observe(infoContainer);

let storedIndex=-1;
let isSame=-1;
let runTimeout=[];

let getQuote = () => {
    do{
        index=Math.floor(Math.random()*(quotes.length)); 
    } while(index===isSame || index===localStorage.getItem('index'));
    localStorage.setItem('index', index);
        runTimeout.forEach((timeout)=>{clearTimeout(timeout)});
        runTimeout=[];
        quotation.innerText='';
        let str=quotes[index].quote;
        let arr=str.split('');
        arr.forEach((letter,idx)=>{
        let timeout=setTimeout(()=>{
        quotation.innerText=quotation.innerText+letter;
        },10*idx);runTimeout.push(timeout);})
        author.innerText='\u2014'+' '+quotes[index].author;
        isSame=index;
    }
    
quoteContainer.addEventListener('click', () => {
   getQuote();
});

subLinks.forEach((link)=> {
    link.addEventListener('click', scrollToTop)
});

function scrollToTop(){
    function step(){
        window.scrollBy(0,-30);
        if(window.scrollY>0){ requestAnimationFrame(step)}
    } requestAnimationFrame(step)
};

window.addEventListener('load', () => {
    getQuote();
});
