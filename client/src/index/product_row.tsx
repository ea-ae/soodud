import React from 'react';
import { useEffect, useState } from 'react';
import Popup from 'reactjs-popup';
import ECharts from 'echarts-for-react';

import { QueryEvents, DetailedProduct, Product, Price, Discount } from './api';
import CloseButton from './buttons';


const ProductRow = (props: {stores: string[], product: Product, item_layout: string}) => {
    const cheapest = Math.min(...props.stores.map(store => props.product.prices[store.toLowerCase()]?.actualPrice ?? Infinity));

    const row = (
        <div className="group flex justify-center md:justify-end
                        items-center justify-items-center flex-wrap md:flex-nowrap
                        mx-1.5 sm:mx-3 lg:mx-5 mb-2 md:mb-1 py-0.5 pb-2 md:pb-1
                        border-0 border-b-[1px] border-neutral-200">
            <ProductName name={props.product.name} />
            {
                props.stores.sort().map(store => {
                    let storeName = store.toLowerCase();
                    let price = props.product.prices[storeName];
                    let is_cheapest = price?.actualPrice == cheapest;
                    return <ProductPrice key={storeName} price={price} cheapest={is_cheapest} item_layout={props.item_layout} />;
                })
            }
        </div>
    );

    return (
        <Popup trigger={row} modal>
            {(onClose: () => void) => (
                <ProductDetail onClose={onClose} product={props.product} />
            )}
        </Popup>
    );
}

const ProductDetail = (props: {onClose: () => void, product: Product}) => { // mx-1.5 my-10 sm:m-6 md:m-12 lg:m-20 xl:m-32
    const [error, setError] = useState<{message: string} | null>(null);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);
    const [data, setData] = useState<DetailedProduct | null>(null);

    const fetchProductDetails = (events: QueryEvents, productId: number) => {
        const url = `${location.protocol}//${location.hostname}:8001/api/v1/products/${productId}/`;
        fetch(url, {method: 'GET', headers: {'Content-Type': 'text/plain'}})
            .then(res => res.json())
            .then(events.onSuccess, events.onError)
    }

    const getProduct = (productId: number) => fetchProductDetails(
        {
            onSuccess: res => { setData(res); setError(null); setIsLoaded(true); },
            onError: err => { setData(null); setError(err); setIsLoaded(true); }
        },
        productId
    );

    useEffect(() => {
        getProduct(props.product.id);
    }, [props.product]);

    let details = <></>;
    if (isLoaded && !error) {
        // details = <p>{(data as DetailedProduct).name}</p>;
        details = <PriceHistoryChart productName={data!.name} />;
    } else {
        details = <p>Laeme...</p>;
    }

    return (
        <div className="shadow-xl border w-[90vw] md:w-[80vw] xl:w-[60vw] bg-stone-50 font-main text-neutral-800">
            <CloseButton onClose={props.onClose} />
            <div className="flex flex-col justify-center items-center p-1.5 sm:p-5 pt-10">
                <p className="flex-grow text-center font-semibold">{props.product.name}</p>
                <p>{props.product.id}</p>
                {details}
            </div>
        </div>
    );
}

const PriceHistoryChart = (props: {productName: string}) => {
    let base = +new Date(2022, 1, 1);
    let oneDay = 24 * 3600 * 1000;

    const getData = () => {
        let date = [];
        let data = [];
        let last_data = 10;
        for (let i = 1; i < 90; i++) {
            var now = new Date((base += oneDay));
            date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'));
            let new_data = last_data + (Math.random() * 0.6 - 0.2);
            last_data = new_data;
            data.push(Number(new_data).toFixed(2));
        }
        return [date, data];
    }

    let [date, data] = getData();
    let [date2, data2] = getData();
    let [date3, data3] = getData();
    let [date4, data4] = getData();

    const generateData = () => {

    }

    let options = {
        grid: { top: 8, right: 8, bottom: 70, left: 40 },
        toolbox: { feature: { restore: {} } },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: date,
        },
        yAxis: {
            type: 'value',
            scale: true,
            boundaryGap: [0, '100%'],
            axisLabel: { formatter: '{value}€' }
        },
        dataZoom: [
            {
                type: 'inside',
                start: 0,
                end: 100,
            },
            {
                start: 0,
                end: 100,
            },
        ],
        tooltip: {
            trigger: 'axis',
        },
        series: [
            {
                data: data,
                name: 'Coop',
                type: 'line',
                lineStyle: {color: '#0070cc'},
                itemStyle: {color: '#0070cc'},
                symbol: 'none',
                sampling: 'lttb',
            },
            {
                data: data2,
                name: 'Prisma',
                type: 'line',
                lineStyle: {color: '#088c44'},
                itemStyle: {color: '#088c44'},
                symbol: 'none',
                sampling: 'lttb',
            },
            {
                data: data3,
                name: 'Rimi',
                type: 'line',
                lineStyle: {color: '#d72323'},
                itemStyle: {color: '#d72323'},
                symbol: 'none',
                sampling: 'lttb',
            },
            {
                data: data4,
                name: 'Selver',
                type: 'line',
                lineStyle: {color: '#e8ce07'},
                itemStyle: {color: '#e8ce07'},
                symbol: 'none',
                sampling: 'lttb',
            },
        ],
    };

    return <ECharts option={options} style={{width: '100%'}} />
}

const ProductName = (props: {name: string}) => {
    return (
        <div className="flex-grow basis-full md:basis-auto cursor-pointer inline-block md:mr-6
                        text-center md:text-right text-xs lg:text-sm
                        group-hover:text-blue-500 font-semibold">
            {props.name}
        </div>
    );
}

const ProductPrice = (props: {price: Price, cheapest: boolean, item_layout: string}) => {
    let color = 'transparent';
    const priceStyle = ['py-2', props.item_layout].join(' ');

    if (props.price == null) { // store doesn't contain product
        return <div className={[priceStyle, props.item_layout, color].join(' ')}>-</div>;
    }

    switch (props.price.discount) {
        case Discount.None:
            color = 'bg-stone-100'
            break;
        case Discount.Normal:
            color = 'bg-yellow-400';
            break;
        case Discount.Member:
            color = 'bg-orange-400';
    }
    return (
        <div className={[priceStyle, color, props.cheapest ? 'font-bold' : ''].join(' ')}>
            {props.price.actualPrice}
        </div>
    );
}

export default ProductRow;
