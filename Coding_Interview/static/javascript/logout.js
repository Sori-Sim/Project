function showAlert(event) {
    alert("You have successfully logged out!!");
}

const logoutLink = document.getElementById("logout");
logoutLink.addEventListener("click", showAlert);