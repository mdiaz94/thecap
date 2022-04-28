var authorSearch;
var articleSearch;
var searchToggle;

document.addEventListener('DOMContentLoaded', function(){ 
    authorSearch = document.getElementById('authorSearch');
    articleSearch = document.getElementById('articleSearch');
    authorSearch.style.setProperty('display','none','important');
    searchToggle = 0;
}, false);

function toggleSearch(){
    if (searchToggle == 0) {
        authorSearch.style.setProperty('display','block','important');
        articleSearch.style.setProperty('display','none','important');
        searchToggle = 1;
    }
    else {
        authorSearch.style.setProperty('display','none','important');
        articleSearch.style.setProperty('display','block','important');
        searchToggle = 0;
    }
}