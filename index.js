document.addEventListener("DOMContentLoaded", () => {


  const burgerIcon = document.querySelector(".burger-icon");
  const rightNav = document.querySelector(".right-nav");

  burgerIcon.addEventListener("click", () => {
    rightNav.classList.toggle("active");
  });

  document.addEventListener("click", (event) => {
    if (!rightNav.contains(event.target) && !burgerIcon.contains(event.target)) {
      rightNav.classList.remove("active");
    }
  });
});
