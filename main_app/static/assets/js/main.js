/*-- off canvas menu start--*/
let openNav = document.getElementById("open-sidenav");
let closeNav = document.getElementById("close-sidenav");
let sideNav = document.getElementById("sidenav");
let sideNavWrap = document.getElementById("sidenav-wrap");
openNav.addEventListener("click", function() {
    openSidenavFunc(event,sideNav,sideNavWrap);
});
closeNav.addEventListener("click", function() {
    closeSidenavFunc(event,sideNav,sideNavWrap);
});
function openSidenavFunc(event,sideNav,sideNavWrap) {
     event.preventDefault();
     sideNav.style.left = "0";
     sideNavWrap.classList.add('sidenav-active');
 }
function closeSidenavFunc(event,sideNav,sideNavWrap) {
    event.preventDefault();
    let sideNavClosePos = "-" + sideNav.offsetWidth + "px";
    sideNav.style.left = sideNavClosePos;
    sideNavWrap.classList.remove('sidenav-active');
}
/*-- off canvas menu end--*/
/*-- Sticky Menu Start--*/
let primaryNavbar = document.querySelector('#primary-navbar');
let navChangePoint = 100;
function stickyNav() {
	if (window.scrollY >= navChangePoint) {
		primaryNavbar.classList.add('shadow-sm');
	} else {
		primaryNavbar.classList.remove('shadow-sm');
	}
}
window.addEventListener('scroll', stickyNav);
/*-- Sticky Menu End--*/
/*-- testimonial slider start --*/
document.addEventListener( 'DOMContentLoaded', function () {
    new Splide( '.splide', {
        type   : 'loop',
        arrows:false,
        pagination:true,
        focus:0,
        perMove:1,
        autoplay:true,
        interval:'3000',
        gap:'1rem',
        padding: {
            left : '4rem',
            right: '4rem',
        },
        perPage: 3,
        breakpoints: {
            992: {
                perPage: 2,
                padding: {
                    left : '2rem',
                    right: '2rem',
                },
            },
            640: {
                perPage: 1,
                padding: {
                    left : '1rem',
                    right: '1rem',
                },
            },
        }
    }).mount();
} );
/*-- testimonial slider end --*/