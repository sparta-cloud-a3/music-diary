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

<<<<<<< HEAD
function click_card() {
    location.href = "diary"
}

=======
>>>>>>> b93d0242fbb6534ab88906127dd56ae2079dc360
function listing() {
    $.ajax({
        type: "GET",
        url: "/diaries",
        data: {},
        success: function (response) {
            let diaries = response['diaries'];
            for (let i = 0; i < diaries.length; i++) {
<<<<<<< HEAD
=======
                let post_id = diaries[i]['post_id'];
>>>>>>> b93d0242fbb6534ab88906127dd56ae2079dc360
                let title = diaries[i]['title'];
                let date = diaries[i]['date'];
                let album_art = diaries[i]['album_art'];

<<<<<<< HEAD
                let temp_html = `<div class="card" onclick="click_card()">
                                                <img class="card-img-top"
                                                     src=${album_art}
                                                     alt="Card image cap">
                                                <div class="card-body">
                                                    <h5 class="card-title">${title}</h5>
                                                    <p class="card-text"><small class="text-muted">${date}</small></p>
                                                </div>
                                            </div>`;
=======
                let temp_html = `<div class="card" onclick="location.href='/diary/${post_id}'">
                                        <img class="card-img-top"
                                             src=${album_art}
                                             alt="Card image cap">
                                        <div class="card-body" id="card-box" name="card-box">
                                            <h5 class="card-title" id="title name="title">${title}</h5>
                                            <p class="card-text"><small class="text-muted">${date}</small></p>
                                        </div>
                                 </div>`;

>>>>>>> b93d0242fbb6534ab88906127dd56ae2079dc360
                $('#diaries-box').append(temp_html);

            }

        }
<<<<<<< HEAD
    })
}
=======
    });
}


>>>>>>> b93d0242fbb6534ab88906127dd56ae2079dc360
