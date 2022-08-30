let toggle = document.querySelector('.toggle');
let sidebar = document.querySelector('.sidebar');
let main = document.querySelector('.main');


toggle.onclick = function(){
    sidebar.classList.toggle('active');
    main.classList.toggle('active');
    }


    // dark main window
// let listItem = document.querySelectorAll('.for-dark');
//
// listItem.onmouseover = function (){
//     main.classList.toggle('dark');
// }
//
//
