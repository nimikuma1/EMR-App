$("#prior-auth-form").submit(function(event) {
                event.preventDefault();
                var selectedMember = $('#member-dropdown').val()
                $.ajax({
                    type: "POST",
                    url: "/priorauth",
                    contentType: "application/json",
                    data: JSON.stringify({
                        member: selectedMember
                    }),
                    success: function(response) {
                        var answer = response.answer;
                        $("#answer").text("Answer: " + answer);
                    },
                    error: function(error) {
                        console.log(error);
                    },
                });
            });