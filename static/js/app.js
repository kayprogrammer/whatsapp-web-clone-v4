// Dropdown Right Side
$(document).on('click', "#dropDown", function (event) {
    $(".drop").toggle(400);
    event.stopPropagation();
});

$(".drop").click(function (event) {
    event.stopPropagation();
});

$(document).click(function () {
    $(".drop").fadeOut();
});


// Popup Conversation
$(document).on('click', "#chat-popup", function (e) {
    $(".popup").toggle(700);
    e.stopPropagation();
});

$(document).on('click', ".popup", function(e) {
    e.stopPropagation();
});

$(document).click(function () {
    $(".popup").fadeOut();
});


// Dropdown LeftSide
$(document).ready(function () {
    $("#dropDown2").click(function (event) {
        $(".dropLeft").toggle(400);
        event.stopPropagation();
    });
});

$(".dropLeft").click(function (event) {
    event.stopPropagation();
});

$(document).click(function () {
    $(".dropLeft").fadeOut();
});


// Emoji 
$(document).on('click', "#emoji-icon", function () {
    $("#emoji-wrap").addClass("emojis__wrapper--active");
    $(".hidden").show();
    $('.send-message').focus()
});
$(document).on('click', "#emoji-remove-icon", function () {
    $("#emoji-wrap").removeClass("emojis__wrapper--active");
    $(".hidden").hide();
    $('.send-message').focus()
});


$(document).ready(function () {
    $("#closeChat").click(function () {
        $(".chat-list").removeClass("active");
    });
});

const moon = document.getElementById("moon")

moon.onclick = function () {
    document.body.classList.toggle("light-theme");
    if (document.body.classList.contains("light-theme")) {
        moon.src = "images/Moon-1.png";
    } else {
        moon.src = "images/Sun-1.png";
    }
}

const select = document.querySelectorAll('.chat-list')

function active() {
    select.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}
select.forEach(l => l.addEventListener("click", active))


// Open new chat from home
function openForm() {
    document.getElementById("Newchat").style.display = "block";
    document.getElementById("leftSid").style.display = "none";
}

function closeForm() {
    document.getElementById("leftSid").style.display = "block";
    document.getElementById("Newchat").style.display = "none";
}


function openRightSide(e) {
    var phone = $(e).data('phone')
    var unread_count_element = $(e).children('.h-text').children('.message-chat').children().children('div').children('span')
     
    $.ajax({
        url: "/chat/show-direct-messages",
        type: "POST",
        data: {
            "phone": phone,
        },
        dataType: "json",
        success: function(response){
            console.log(response)
            if (response.success){
                document.getElementById("rightSide").style.display = "flex";
                document.getElementById("Intro-Left").style.display = "none";
                $('#rightSide').html(response.html_data)
                unread_count_element.fadeOut(100)
                var chat = document.getElementById('last-msg')
                if (chat){
                    chat.scrollIntoView()
                }

            }
        }
    })

}

function closeRightSide() {
    document.getElementById("Intro-Left").style.display = "block";
    document.getElementById("rightSide").style.display = "none";
    document.getElementById("ChatAbout").style.display = "none";
    document.getElementById("search-message").style.display = "none";
}


// Open chatAbout from new chat
function openChatAbout() {
    document.getElementById("ChatAbout").style.display = "block";
}

function closeChatAbout() {
    document.getElementById("ChatAbout").style.display = "none";
}


// Open Search from new chat
function openSearch() {
    document.getElementById("search-message").style.display = "block";
}

function closeSearch() {
    document.getElementById("search-message").style.display = "none";
}


// Open group from new chat
function openGroup() {
    document.getElementById("group").style.display = "block";
    document.getElementById("Newchat").style.display = "none";
}

function closeGroup() {
    document.getElementById("Newchat").style.display = "block";
    document.getElementById("group").style.display = "none";
}


// Open Group from list item
function openGrp() {
    document.getElementById("group").style.display = "block";
    document.getElementById("leftSid").style.display = "none";
}

function closeGroup() {
    document.getElementById("leftSid").style.display = "block";
    document.getElementById("group").style.display = "none";
}


// Open Group from list item
function openStarred() {
    document.getElementById("starred").style.display = "block";
    document.getElementById("leftSid").style.display = "none";
}

function closeStarred() {
    document.getElementById("leftSid").style.display = "block";
    document.getElementById("starred").style.display = "none";
}


// Open Settings from list item
function openSettings() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("leftSid").style.display = "none";
}

function closeSettings() {
    document.getElementById("leftSid").style.display = "block";
    document.getElementById("settings").style.display = "none";
}


// Open profile from settings
function openProfile() {
    document.getElementById("profile").style.display = "block";
    document.getElementById("settings").style.display = "none";
}

function closeProfile() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("profile").style.display = "none";
}


// Open notifications from settings
function openNotifications() {
    document.getElementById("notifications").style.display = "block";
    document.getElementById("settings").style.display = "none";
}

function closeNotifications() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("notifications").style.display = "none";
}


// Open privacy from settings
function openPrivacy() {
    document.getElementById("privacy").style.display = "block";
    document.getElementById("settings").style.display = "none";
}

function closePrivacy() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("privacy").style.display = "none";
}


// Open Last seen from privacy
function openLast() {
    document.getElementById("last-seen").style.display = "block";
    document.getElementById("privacy").style.display = "none";
}

function closeLast() {
    document.getElementById("privacy").style.display = "block";
    document.getElementById("last-seen").style.display = "none";
}

// Open Profile photo from privacy
function openPhoto() {
    document.getElementById("p-photo").style.display = "block";
    document.getElementById("privacy").style.display = "none";
}

function closePhoto() {
    document.getElementById("privacy").style.display = "block";
    document.getElementById("p-photo").style.display = "none";
}


// Open About from privacy
function openAbout() {
    document.getElementById("about").style.display = "block";
    document.getElementById("privacy").style.display = "none";
}

function closeAbout() {
    document.getElementById("privacy").style.display = "block";
    document.getElementById("about").style.display = "none";
}


// Open D-message from privacy
function openDmessage() {
    document.getElementById("D-message").style.display = "block";
    document.getElementById("privacy").style.display = "none";
}

function closeDmessage() {
    document.getElementById("privacy").style.display = "block";
    document.getElementById("D-message").style.display = "none";
}


// Open groups from privacy
function openGroups() {
    document.getElementById("groups").style.display = "block";
    document.getElementById("privacy").style.display = "none";
}

function closeGroups() {
    document.getElementById("privacy").style.display = "block";
    document.getElementById("groups").style.display = "none";
}


// Open blocked Contact from privacy
function openBlock() {
    document.getElementById("blocks").style.display = "block";
    document.getElementById("privacy").style.display = "none";
}

function closeBlock() {
    document.getElementById("privacy").style.display = "block";
    document.getElementById("blocks").style.display = "none";
}


// Open Security from settings
function openSecurity() {
    document.getElementById("security").style.display = "block";
    document.getElementById("settings").style.display = "none";
}

function closeSecurity() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("security").style.display = "none";
}


// Open Chat Wallpaper from settings
function openWallpaper() {
    document.getElementById("wallpaper").style.display = "block";
    document.getElementById("settings").style.display = "none";
}

function closeWallpaper() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("wallpaper").style.display = "none";
}


// Open Request Account Info from settings
function openRequest() {
    document.getElementById("request").style.display = "block";
    document.getElementById("settings").style.display = "none";
}

function closeRequest() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("request").style.display = "none";
}


// Open Help from settings
function openHelp() {
    document.getElementById("help").style.display = "block";
    document.getElementById("settings").style.display = "none";
}

function closeHelp() {
    document.getElementById("settings").style.display = "block";
    document.getElementById("help").style.display = "none";
}


// Open new chat from home
function openStatus() {
    document.getElementById("status").style.display = "block";
    document.getElementById("rightStatus").style.display = "block";
    document.getElementById("Intro-Left").style.display = "none";
    document.getElementById("right").style.display = "none";
    document.getElementById("leftSid").style.display = "none";
    document.getElementById("rightSide").style.display = "none";
}

function closeStatus() {
    document.getElementById("leftSid").style.display = "block";
    document.getElementById("Intro-Left").style.display = "block";
    document.getElementById("right").style.display = "flex";
    document.getElementById("rightSide").style.display = "none";
    document.getElementById("status").style.display = "none";
    document.getElementById("rightStatus").style.display = "none";
}