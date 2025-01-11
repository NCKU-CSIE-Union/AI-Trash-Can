const char INDEX_HTML[] = R"=====(

<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style  type="text/css">

        *{
            margin: 0;
            padding: 0;
        }
        .header{
            position: absolute;
            top: 0%;
            left: 0%;
            width: 100%;
            height: 10%;
            background-color: rgb(52, 64, 75);
            
        }
        h2{
            font-size: 30px;
            font-weight: 900;
            letter-spacing:2px;
            font-family:'Courier New', Courier, monospace ;
            color: aliceblue;
            padding-left: 20px;
            padding-top: 20px;
        }
        .container{
            text-align: center;
        }
        img{
            max-width: 900px;
            padding-top: 10px;
        }
        button{
            position:absolute;
            left: 50%;
            top:80%;
            width: 10%;
            min-width: 140px;
            height: 70px;
            border-radius: 10px;
            font-size: 30px;
            font-weight: 900;
            padding-top: 10px;
            border: 5px solid rgb(139, 139, 151);
            color: aliceblue;
            background-color: rgb(52, 64, 75);

            transform: translate(-50%);
        }

        
        @media screen and (max-width: 900px) {
            .header {
                height: 70px;
            }
            img{
                max-width: 100%;
                height: auto;
                padding-top: 40px;
            }
        }

        @media screen and (max-width: 500px) {
            img{
                max-width: 100%;
                height: auto;
                padding-top: 100px;
            }
            button{
                height: 60px;
                font-size: 25px;
            }
        }

        
    </style>
    <title>Home Page</title>
  </head>
  <body>
    

    <!-- header -->
    <div class="bg-dark header">
        <h2 class="test" >Home</h2>
    </div>

   
    <div class="container">
        <img src="https://i.imgur.com/BQeY8sG.jpg" href='https://www.freepik.com/vectors/infographic' >
        <button onclick=" location.href='login' ">LOGIN</button>
    </div>

   
  </body>
</html>

)=====";
