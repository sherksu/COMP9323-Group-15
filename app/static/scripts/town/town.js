window.onload = function(){
    var myCanvas = document.getElementById('c1')
    let ctx = myCanvas.getContext('2d')
    let img = new Image();
    let canvasWidth = ctx.canvas.width;
    let canvasHeight = ctx.canvas.height;
    var direction = 3;
    var step = 0;
    img.onload = function(){
        let personWidth = img.width/10;
        let personHeight = img.height/8;
        let x0 = 200;
        let y0 = 600;
        // 在中间画出来就行了
        // 第一步就是把它画出来，非常的简单
        ctx.drawImage(img,personWidth*9,personHeight*7,personWidth,personHeight,x0,y0,personWidth,personHeight);
        document.onkeydown = function(e){
            if(e.keyCode==37){
                    ctx.clearRect(0,0,canvasWidth,canvasHeight)
                if(direction!=0){
                    step=0;
                        ctx.drawImage(img,0,personHeight*5,personWidth,personHeight,x0,y0,personWidth,personHeight);
                    direction=0;
                }else {
                    // 若是同个方向，则开始行走
                    step++;
                     x0-=10;
                    if(step>3){
                        step = 0;
                    }
                    ctx.drawImage(img,step*personWidth,personHeight*5,personWidth,personHeight,x0,y0,personWidth,personHeight);

                }

            } else if(e.keyCode==39){
                    ctx.clearRect(0,0,canvasWidth,canvasHeight)
                    if(direction!=2){
                        step=0;
                        ctx.drawImage(img,personWidth*9,personHeight*7,personWidth,personHeight,x0,y0,personWidth,personHeight);
                        direction=2;
                }else{
                    x0+=10;
                    step++;
                    if(step>3){
                        step = 0;
                    }
                    ctx.drawImage(img,step*personWidth,personHeight*7,personWidth,personHeight,x0,y0,personWidth,personHeight);
                }

            }

        }
    }
    img.src = "/static/image/town/pp.png"
}