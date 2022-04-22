$(document).ready(function () {
    listing();
});

function search() {
    let search_text = $('#search-box').val();
    if (search_text == "") {
        alert("검색어를 입력하세요");
    } else {
        $('#searchform').submit();
    }
}

function listing() {
    $.ajax({
        type: "GET",
        url: "/diaries",
        data: {},
        success: function (response) {
            let diaries = response['diaries'];
            for (let i = 0; i < diaries.length; i++) {
                let post_id = diaries[i]['post_id'];
                let title = diaries[i]['title'];
                let date = diaries[i]['date'];
                let album_art = diaries[i]['album_art'];


                let temp_html = `<div class="card" onclick="location.href='/diary/${post_id}'">
                                        <img class="card-img-top"
                                             src=${album_art}
                                             alt="Card image cap">
                                        <div class="card-body" id="card-box" name="card-box">
                                            <h5 class="card-title" id="title name="title">${title}</h5>
                                            <p class="card-text"><small class="text-muted">${date}</small></p>
                                        </div>
                                 </div>`;

                $('#diaries-box').append(temp_html);

            }

        }
    });
}



