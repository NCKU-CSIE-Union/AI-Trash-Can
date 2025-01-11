const char ADMIN_HTML[] = R"=====(

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
            left: 0%;
            height: 300px;

            min-width: 500px;
        }
        .submit{
            position:absolute;
            left:75%;
            top:25%;
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
        .logout{
            position:absolute;
            right:20px;
            top:20px;
            width: 8%;
            min-width: 120px;
            height: 60px;
            border-radius: 10px;
            font-size: 25px;
            font-weight: 700;
            padding-top: 10px;
            border: 5px solid aliceblue;
            color: aliceblue;
            background-color: rgb(52, 64, 75);
        }

        input{
            position: absolute;
            left: 10%;
            top: 25%;
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

        .check{
            position:absolute;
            left:42.5%;
            bottom: 30%;
            width: 15%;
            min-width: 200px;
            height: 70px;
            border-radius: 10px;
            font-size: 30px;
            font-weight: 900;
            font-family:'Courier New', Courier, monospace ;
            padding-top: 10px;
            border: 5px solid rgb(52, 64, 75);
            color: aliceblue;
            background-color: rgb(52, 64, 75);
        }

        svg{
            position: absolute;
            left:5%;
        }
        .Record{
            position: absolute;
            left:40%;
            top:20px;
        }


        

        
        @media screen and (max-width: 960px) {
            .header {
                height: 70px;
            }
            .logout{
                top:10px;
                min-width: 100px;
                height: 50px;
                font-size: 20px;
                border: 3px solid aliceblue;
            }
        }

        @media screen and (max-width: 500px) {
            
            .submit{
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

            svg{
                width: 30px;
                height: 30px;
            }

            .check{
                min-width: 170px;
                height:50px;
                font-size: 20px;
                left: 25%;
                bottom: 10%;
            }
        }

        
    </style>
    <title>Admin Page</title>
  </head>
  <body>
    

    <!-- header -->
    <div class="bg-dark header">
        <h2 class="test" >Admin</h2>
        <form action='/logout' method='GET'>
            <button class="logout" type="submit">Logout</button>
        </form>
    </div>

   
    <div class="container">
        <form action='/admin' method='POST'>
            <div class="input-group">
                <input name="PASSWORD" placeholder="New Password" type="text" >
                <button class="submit" type="submit">Submit</button>
            </div>
        </form>
        
        <div class="check" onclick="location.href='https://docs.google.com/spreadsheets/d/1Po2Ll1h-KpENLhq1eH1kr00YN-hbdD54NjI8gxoVnw8/edit#gid=1275261346' ">
            <svg xmlns="http://www.w3.org/2000/svg" width="50px" height="50px" fill="currentColor" viewBox="0 0 16 16">
                <path d="M5 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5zM5 8a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm0 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1H5z"/>
                <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z"/>
            </svg>
            <a class="Record">Record</a>
        </div>
    </div>

   
  </body>
</html>

)=====";
