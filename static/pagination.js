var page=1
var results
var currentPage
var currentPageText
var maxPageNumber

document.addEventListener('DOMContentLoaded', function(){ 
    results = document.getElementsByClassName('card');
    document.getElementsByTagName('body')[0].style.display = "block";
    var results1 = document.getElementsByClassName('page1');
    currentPageText = document.getElementById('currentPageText');
    for (var i = 0; i < results.length; i ++) {
        results[i].style.display = 'none';
    }
    for (var i = 0; i < results1.length; i ++) {
        results1[i].style.display = 'block';
    }
    maxPageNumber = parseInt(document.getElementById('maxPageNumber').innerHTML) - 1;
    updateCurrentPageText(page);
}, false);

function showPage(pageInt) {
    for (var i = 0; i < results.length; i ++) {
        results[i].style.display = 'none';
    }
    page = pageInt
    var pageNumber = "page" + page
    currentPage = document.getElementsByClassName(pageNumber);
    for (var i = 0; i < currentPage.length; i ++) {
        currentPage[i].style.display = 'block';
    }
    updateCurrentPageText(page);
}

function previousPage() {
    if (page == 1) {
        return
    }
    for (var i = 0; i < results.length; i ++) {
        results[i].style.display = 'none';
    }
    page = page-1;
    var pageNumber = "page" + page;
    currentPage = document.getElementsByClassName(pageNumber);
    for (var i = 0; i < currentPage.length; i ++) {
        currentPage[i].style.display = 'block';
    }
    updateCurrentPageText(page);
}

function nextPage() {
    if (page == maxPageNumber) {
        return
    }
    for (var i = 0; i < results.length; i ++) {
        results[i].style.display = 'none';
    }
    page = page+1;
    var pageNumber = "page" + page;
    currentPage = document.getElementsByClassName(pageNumber);
    for (var i = 0; i < currentPage.length; i ++) {
        currentPage[i].style.display = 'block';
    }
    updateCurrentPageText(page);
}

function updateCurrentPageText(pageInt){
    if (maxPageNumber == 0){
        pageButton = document.getElementsByClassName('page-link');
        for (var i = 0; i < pageButton.length; i ++) {
            pageButton[i].style.display = 'none';
        }
        return
    }
    currentPageText.innerHTML = "Page " + pageInt + " out of " + maxPageNumber;
    window.focus();
    setTimeout(window.scrollTo({top: 0, behavior: 'smooth'}),1);
}