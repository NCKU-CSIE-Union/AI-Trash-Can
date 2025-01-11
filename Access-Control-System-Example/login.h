const char LOGIN_HTML[] = R"=====(
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
            position: absolute;
            top:20%;
            width: 100%;
            height: 50%;
            background-color: inherit;
        }
        .input-group{
            position: absolute;
            top:10%;
            background-color: rgb(139, 139, 151);
            width: 100%;
            left: auto;
            height: 300px;

            min-width: 500px;
        }
        button{
            position:absolute;
            left:75%;
            top:60%;
            width: 10%;
            min-width: 140px;
            height: 70px;
            border-radius: 10px;
            font-size: 30px;
            font-weight: 900;
            padding-top: 10px;
            border: 5px solid rgb(52, 64, 75);
            color: aliceblue;
            background-color: rgb(52, 64, 75);
            
        }

        input{
            position: absolute;
            left: 10%;
            height: 65px;
            width: 50%;
            border: 5px solid rgb(52, 64, 75);
            border-radius: 10px;
            background-color: rgb(255, 255, 255);

            /* text */
            letter-spacing:1px;
            font-family:'Courier New', Courier, monospace ;
            color: rgb(139, 139, 151);
            padding-left: 20px;
            font-size: 25px;
        }
        input::placeholder{
            letter-spacing:1px;
            font-family:'Courier New', Courier, monospace ;
            color: rgb(139, 139, 151);
            padding-left: 20px;
            font-size: 25px;
        }

        .inp1{
            top:20%;
        }

        .inp2{
            top:60%;
        }

        

        
        @media screen and (max-width: 960px) {
            .header {
                height: 70px;
            }
        }

        @media screen and (max-width: 600px) {
            
            button{
                height: 55px;
                min-width: 100px;
                font-size: 20px;
                left:50%;
            }
            
            input{
                width: 170px;
                height:50px;
                left:5%;
                font-size: 15px;
            }
            input::placeholder{
                font-size: 15px;
            }
        }

        
    </style>
    <title>Login Page</title>
  </head>
  <body>
    

    <!-- header -->
    <div class="bg-dark header">
        <h2 class="test" >Login</h2>
    </div>

   
    <div class="container">
        <div class="input-group">
            <form action='/login' method='POST'>
                <input name="USERNAME" placeholder="Username" type="text" class="inp1">
                <input name="PASSWORD" placeholder="Password" type="text" class="inp2">
                <button type="submit" name='SUBMIT' value='Submit'>Submit</button>
            </form>
        </div>
        
    </div>

   
  </body>
</html>

)=====";
