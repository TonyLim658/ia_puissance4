vsia = false;
botbegin = false;
nbLines = 8;

/*******Fonction pour vérifier que le token peut être envoyé dans l'entete*********/
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/*slow foreach*/
$.fn.ogni = function (f, t) {
    var i = 0;

    function recurse(list) {
        var el = list.shift();
        f.apply(el, [i++, el]) || setTimeout(function () {
            list.length && recurse(list)
        }, t)
    }
    this.length && recurse(this.toArray());
    return this
}

showVictory = function(winArray){
    console.log(winArray)
    $.each(winArray, function () {
        line = this[0];
        column = this[1];

        $('.line.'+line).find('.placement.pos.'+column).addClass('winToken');
    });
}

/*******recherche/affichage de résultat d'un algo par ajax*********/
function tokenPress(column) {

    token = $('.pos.active').attr('class').split(' ')[2]

    var line = 0;
    var lastCase = null;

    $('#posBtn'+column).addClass('hiddenPlus');

    $('.placement.pos.'+column).ogni(function(i, obj) {
        class_name = $(this).attr('class');
        if (class_name == 'placement pos '+column) {
            if (lastCase != null){
                lastCase.removeClass(token);
            }
            lastCase = $(this);
            line = i;
            lastCase.addClass(token);
        }
    }, 25);

    /*Entrer le token csrf dans le header si la route est sécurisé*/
      var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
      /*console.log("csrf token : "+csrftoken);*/
      $.ajaxSetup({
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
      });

    setTimeout(function () {
            $.ajax({
                type: 'POST',
                url: './play',
                data: {
                    col: column,
                    line: line,
                    token: token,
                },
                success: function (data) {

                    //stateG 1 : fin de partie ; 2 : tour suivant ; 3 : rejouer
                    //stateEOG -1 : jaune ; 0 : égalité ; 1 : rouges

                    console.log(data)

                    if (data.state == 1){

                        $('.pos.btn').addClass('hidden');
                        showVictory(JSON.parse(data.winPos));

                        if (vsia){
                            if(botbegin){
                                if (data.stateEOG == -1){
                                    $('#messageBox').text("Vous avez gagné ! ");
                                }
                                else if(data.stateEOG == 0){
                                    $('#messageBox').text("Vous avez fait égalité ! ");
                                }
                                else{
                                    $('#messageBox').text("Le robot a gagné ! ");
                                }
                            }
                            else {
                                if (data.stateEOG == -1){
                                    $('#messageBox').text("Le robot a gagné ! ");
                                }
                                else if(data.stateEOG == 0){
                                    $('#messageBox').text("Vous avez fait égalité ! ");
                                }
                                else{
                                    $('#messageBox').text("Vous avez gagné ! ");
                                }
                            }
                        }
                        else {
                            if (data.stateEOG == -1){
                                $('#messageBox').text("Le joueur jaune a gagné ! ");
                            }
                            else if(data.stateEOG == 0){
                                $('#messageBox').text("Vous avez fait égalité ! ");
                            }
                            else{
                                $('#messageBox').text("Le joueur rouge a gagné ! ");
                            }
                        }

                    }
                    else if(data.state == 2){
                        if (vsia){
                            $('#messageBox').text("Au tour du bot de jouer ! ");

                            $('.pos.btn').addClass('hidden');

                            if(data.token == "RED_TOKEN"){
                                $('.view.pos.RED_TOKEN').addClass('active');
                                $('.view.pos.YELLOW_TOKEN').removeClass('active');

                                $('.pos.btn').removeClass('YELLOW_TOKEN');
                                $('.pos.btn').addClass('RED_TOKEN');
                            }
                            else{
                                $('.view.pos.YELLOW_TOKEN').addClass('active');
                                $('.view.pos.RED_TOKEN').removeClass('active');

                                $('.pos.btn').removeClass('RED_TOKEN');
                                $('.pos.btn').addClass('YELLOW_TOKEN');
                            }

                            simulateBotPlaying(data.token);

                        }
                        else {

                            if(data.token == "RED_TOKEN"){

                                $('#messageBox').text("Au tour du joueur rouge de jouer ! ");

                                $('.view.pos.RED_TOKEN').addClass('active');
                                $('.view.pos.YELLOW_TOKEN').removeClass('active');

                                $('.pos.btn').removeClass('YELLOW_TOKEN');
                                $('.pos.btn').addClass('RED_TOKEN');
                            }
                            else{

                                $('#messageBox').text("Au tour du joueur jaune de jouer ! ");

                                $('.view.pos.YELLOW_TOKEN').addClass('active');
                                $('.view.pos.RED_TOKEN').removeClass('active');

                                $('.pos.btn').removeClass('RED_TOKEN');
                                $('.pos.btn').addClass('YELLOW_TOKEN');
                            }

                        }

                        if (line != 0) $('#posBtn'+column).removeClass('hiddenPlus');
                    }
                    else{
                        $('#messageBox').text("Position impossible, vous devez rejouer un autre coup ! ");
                    }

                },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    alert("Status: " + textStatus); alert("Error: " + errorThrown);
                }

              });
        }, 25*nbLines);



};

function simulateBotPlaying(token)
{
    /*Entrer le token csrf dans le header si la route est sécurisé*/
      var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
      /*console.log("csrf token : "+csrftoken);*/
      $.ajaxSetup({
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
      });

    $.ajax({
        type: 'POST',
        url: './bot_playing',
        data: {
            token: token,
        },
        success: function (data) {

            //stateG 1 : fin de partie ; 2 : tour suivant ; 3 : rejouer
            //stateEOG -1 : jaune ; 0 : égalité ; 1 : rouges

            console.log(data)

            var column = data.posJ;
            var lastCase = null;
            var line = 0;
            $('.placement.pos.'+column).ogni(function(i, obj) {
                class_name = $(this).attr('class');
                if (class_name == 'placement pos '+column) {
                    if (lastCase != null){
                        lastCase.removeClass(token);
                    }
                    lastCase = $(this);
                    lastCase.addClass(token);
                    line = i;
                }
            }, 25);

            setTimeout(function () {
                if (line == 0) $('#posBtn'+column).addClass('hiddenPlus');
            }, 25*nbLines)

            if (data.state == 1){

                showVictory(JSON.parse(data.winPos));

                if(botbegin){
                    if (data.stateEOG == -1){
                        $('#messageBox').text("Vous avez gagné ! ");
                    }
                    else if(data.stateEOG == 0){
                        $('#messageBox').text("Vous avez égalité ! ");
                    }
                    else{
                        $('#messageBox').text("Le robot a gagné ! ");
                    }
                }
                else {
                    if (data.stateEOG == -1){
                        $('#messageBox').text("Le robot a gagné ! ");
                    }
                    else if(data.stateEOG == 0){
                        $('#messageBox').text("Vous avez égalité ! ");
                    }
                    else{
                        $('#messageBox').text("Vous avez gagné ! ");
                    }
                }
            }
            else if(data.state == 2){

                $('#messageBox').text("A votre tour de jouer ! ");

                if(data.token == "RED_TOKEN"){
                    $('.view.pos.RED_TOKEN').addClass('active');
                    $('.view.pos.YELLOW_TOKEN').removeClass('active');

                    $('.pos.btn').removeClass('YELLOW_TOKEN');
                    $('.pos.btn').addClass('RED_TOKEN');
                }
                else{
                    $('.view.pos.YELLOW_TOKEN').addClass('active');
                    $('.view.pos.RED_TOKEN').removeClass('active');

                    $('.pos.btn').removeClass('RED_TOKEN');
                    $('.pos.btn').addClass('YELLOW_TOKEN');
                }

                $('.pos.btn').removeClass('hidden');

            }

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus); alert("Error: " + errorThrown);
        }

  });
}

reloadGame = function (ia=false,begin=false){

    /*Entrer le token csrf dans le header si la route est sécurisé*/
      var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
      /*console.log("csrf token : "+csrftoken);*/
      $.ajaxSetup({
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                  xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
          }
      });

    $.ajax({
        type: 'POST',
        url: './reload',
        data: {},
        success: function (data) {

            if (data.ok){
                $('.placement').each(function(i, obj) {
                    $(this).removeClass('RED_TOKEN');
                    $(this).removeClass('YELLOW_TOKEN');
                    $(this).removeClass('winToken');
                });

                vsia = ia;
                botbegin = begin;

                $('.view.pos.RED_TOKEN').addClass('active');
                $('.view.pos.YELLOW_TOKEN').removeClass('active');

                $('.pos.btn').removeClass('YELLOW_TOKEN');
                $('.pos.btn').removeClass('hidden');
                $('.pos.btn').removeClass('hiddenPlus');
                $('.pos.btn').addClass('RED_TOKEN');

                if(ia){
                    if (begin){
                        $('#messageBox').text("Le robot commencer ! ");
                        simulateBotPlaying("RED_TOKEN");
                    }
                    else {
                        $('#messageBox').text("Vous pouvez commencer ! ");
                    }
                }
                else{
                    $('#messageBox').text("Au tour du joueur rouge jouer ! ");
                }
            }

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("Status: " + textStatus); alert("Error: " + errorThrown);
        }

      });
}

gameVsIa = function (){
    $('#whoBegin').modal('show');
}

iaBegin = function (botPos){
    reloadGame(true, botPos);
}

gameVsPlayer = function (){
    reloadGame(false, false);
}



