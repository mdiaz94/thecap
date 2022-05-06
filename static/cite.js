function copyAPA() {
    var apaCite = document.getElementById('apaCite')
    navigator.clipboard.writeText(apaCite.value);
    alert("APA Citation has been copied to your clipboard");
}

function copyMLA() {
    var mlaCite = document.getElementById('mlaCite')
    navigator.clipboard.writeText(mlaCite.value);
    alert("MLA Citation has been copied to your clipboard");
}