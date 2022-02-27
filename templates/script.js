const startingMinutes = 5;
let time = startingMinutes * 60;

const countDownEl = document.getElementById('countDown');

setInterval(updateCountdown, 1000);

function updateCountdown()
{
    const minutes = Math.floor(time/60);
    let seconds = time % 60;

    seconds = seconds < 10 ? '0' + seconds : seconds;

    countDownEl.innerHTML = `${minutes}:${seconds}`;

    if(time>0)
    {
        time--;
    }
}

//generating random boolean value(True or False)
function getRandomBooolean()
{
    randomBool = Math.random() < 0.5;
    return randomBool;
}

console.log(getRandomBooolean());
