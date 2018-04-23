$(document).ready(function () {
    let userTypeSelect = $("select");
    userTypeSelect.on("change", function () {
        let element = this.value;

        let profiles = document.getElementsByClassName("profile");
        for (let i = 0; i < profiles.length; i++) {
            if (profiles[i].getAttribute('id') === element)
                profiles[i].style.display = 'block';
            else
                profiles[i].style.display = 'none'
        }
    });
});