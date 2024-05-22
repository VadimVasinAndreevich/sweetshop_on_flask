function operation(price, ind)
{
    price1 = parseInt(price);
    count = parseInt(document.getElementById(`count${ind}`).value);
    priceTotal = price1 * count;
    document.getElementById(`number${ind}`).innerHTML = `Цена за ${count} шт.: ${priceTotal} руб.`;
}


function operationOne()
{
    list = document.getElementsByTagName("p");
    total = 0;
    console.log(list);
    for (let i = 0; i < list.length; i++)
    {
        if (list[i].id && list[i].id != 'total')
        {
            operator = list[i].id;
            string = document.getElementById(operator).innerHTML;
            num = parseInt(string.slice(string.indexOf(":")+2, string.indexOf("р")-1));
            total += num;
        }
    }
    document.getElementById("total").innerHTML = `Итоговая цена: ${total} руб.`;
}