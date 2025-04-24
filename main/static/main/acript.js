const showBtn = document.querySelectorAll(".showBtn")

if(!!showBtn) {
    showBtn.forEach((item, index) => {
        item.addEventListener("click", () => {
            item.nextElementSibling.classList.toggle("!flex")
        })
    })
}

// ---------------------------------------------------------------

const sendAnApplication = document.querySelector(".sendAnApplication")
const buyBtn = document.querySelectorAll(".buyBtn")

console.log(buyBtn);


buyBtn.forEach((item, index) => {
    if(!!item || !!sendAnApplication) {
        item.addEventListener("click", () => {
            sendAnApplication.classList.add("!flex")
        })
        
        sendAnApplication.addEventListener("click", (e) => {
            if (!e.target.closest(".sendAnApplicationBody")) {
                sendAnApplication.classList.remove("!flex")
            }
        })
    }
})

// ---------------------------------------------------------------

const burgerBody = document.querySelector("#burgerBody")
const burgerOpen = document.querySelector("#burgerOpen")
const burgerClose = document.querySelector("#burgerClose")

if(!!burgerBody && !!burgerOpen && !!burgerClose) {
    burgerOpen.addEventListener("click", () => {
        burgerBody.classList.toggle("max-800px:translate-x-[-100%]")
    })
    
    burgerClose.addEventListener("click", () => {
        burgerBody.classList.toggle("max-800px:translate-x-[-100%]")
    })
}

// ---------------------------------------------------------------

const priceScrollerBtn = document.querySelector("#priceScrollerBtn")
const priceScrollerMin = document.querySelector("#priceScrollerMin")
const priceMin = document.querySelector("#priceMin")
const priceMax = document.querySelector("#priceMax")
const maxPrice = 5000
let fix = false

if(!!priceScrollerBtn && !!priceScrollerMin && !!priceMin && !!priceMax) {
    priceMax.innerText = priceDote(maxPrice)

    priceScrollerBtn.addEventListener("mousedown", () => fix = true)
    document.addEventListener("mouseup", () => fix = false)
    document.addEventListener("mousemove", (e) => {
        if(!!fix) {
            let a = e.clientX - priceScrollerBtn.parentElement.getBoundingClientRect().x
            if((a - 8) <= priceScrollerBtn.parentElement.getBoundingClientRect().width && (a - 8) >= 0) {
                priceScrollerBtn.style.left = `${a - 8}px`
                priceScrollerMin.style.width = `${a}px`            
            }
            if((a - 8) <= 0) {
                priceScrollerBtn.style.left = `0px`
                priceScrollerMin.style.width = `0px`
            }
            if((a - 8) >= priceScrollerBtn.parentElement.getBoundingClientRect().width) {
                priceScrollerBtn.style.left = `263px`
                priceScrollerMin.style.width = `263px`
            }
        }
    })
}

function priceDote(price) {
    let a =  String(price).split("").flatMap((item, index) => {
        if(index % 3 == 0) return [item, "."]
        else return item
    }).reverse()
    return a.splice(1, a.length).reverse().join("")
}
