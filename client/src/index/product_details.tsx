import React from 'react';
import { useEffect, useState } from 'react';
import ECharts from 'echarts-for-react';

import { QueryEvents, DetailedProduct, DetailedStoreProduct, DetailedPrice, Product } from './api';
import CloseButton from './buttons';


const ProductDetails = (props: {onClose: () => void, product: Product}) => { // mx-1.5 my-10 sm:m-6 md:m-12 lg:m-20 xl:m-32
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
        let title = '';
        let names: JSX.Element[] = [];
        data!.store_products.map(sp => {
            if (sp.name == props.product.name) {
                title = `${props.product.name} (${sp.store_name})`;
            } else {
                const name = `${sp.name} (${sp.store_name})`;

                names.push(
                    <p key={name} className="text-neutral-600 text-center text-xs md:text-sm leading-4">{name}</p>
                );
            }
        });

        details = (
            <>
            <p className="flex-grow mt-2 text-center font-semibold">{title}</p>
            {names}
            <PriceHistoryChart products={data!.store_products} />
            </>
        );
    } else {
        details = (
            <>
            <p className="flex-grow mt-2 text-center font-semibold">{props.product.name}</p>
            <p>Laeme...</p>
            </>
        );
    }

    return (
        <div className="shadow-xl border w-[90vw] md:w-[80vw] xl:w-[60vw] bg-stone-50 font-main text-neutral-800">
            <CloseButton onClose={props.onClose} />
            <div className="flex flex-col justify-center items-center p-1.5 sm:p-5 pt-10 text-sm sm:text-base">
                {details}
            </div>
        </div>
    );
}

const PriceHistoryChart = (props: {products: DetailedStoreProduct[]}) => {
    const getPriceDate = (startTime: string) => {
        let date = new Date(startTime);
        date.setHours(0, 0, 0, 0);
        return +date;
    }

    let dates: number[] = [];
    props.products.forEach(product => { // create x axis of dates
        product.prices.forEach(price => {
            dates.push(getPriceDate(price.start));
        });
    });

    dates = [...Array.from(new Set(dates))]; // remove duplicate dates and sort
    dates.sort();

    let dateAxis = dates.map(dateNumber => {
        let date = new Date(dateNumber);
        return [date.getFullYear(), date.getMonth() + 1, date.getDate()].join('/');
    });

    let storePrices = props.products.map(product => {
        let priceHistory: (number | null)[] = []
        let priceIndex = 0;
        let lastPrice = null;

        for (let dateIndex = 0; dateIndex < dates.length; dateIndex++) {
            let outOfPrices = priceIndex >= product.prices.length;
            if (!outOfPrices && getPriceDate(product.prices[priceIndex].start) == dates[dateIndex]) {
                let price = product.prices[priceIndex].price;
                priceHistory.push(price);
                lastPrice = price;
                priceIndex++; // price has been assigned, move onto next one
                dateIndex--; // if next price is at the same date, overwrite
            } else {
                priceHistory.push(lastPrice);
            }
        }

        return {
            storeName: product.store_name,
            priceHistory: priceHistory,
        };
    });

    console.log('datessss');
    console.log(dates);

    let series = storePrices.map(storePrice => {
        return {
            name: storePrice.storeName,
            data: storePrice.priceHistory,
            type: 'line',
            // smooth: true,
            // step: true,
            // z index (z) .... todo
            symbol: 'emptyCircle', // none
            animationDuration: 600,
            sampling: 'lttb',
        }
    });

    let options = {
        grid: { top: 8, right: 8, bottom: 70, left: 40 },
        toolbox: { feature: { restore: {} } },
        xAxis: {
            type: 'category',
            boundaryGap: true,
            data: dateAxis,
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
        series: series
        // series: [
        //     {
        //         data: data,
        //         name: 'Coop',
        //         type: 'line',
        //         lineStyle: {color: '#0070cc'},
        //         itemStyle: {color: '#0070cc'},
        //         symbol: 'none',
        //         sampling: 'lttb',
        //     },
        //     {
        //         data: data2,
        //         name: 'Prisma',
        //         type: 'line',
        //         lineStyle: {color: '#088c44'},
        //         itemStyle: {color: '#088c44'},
        //         symbol: 'none',
        //         sampling: 'lttb',
        //     },
        //     {
        //         data: data3,
        //         name: 'Rimi',
        //         type: 'line',
        //         lineStyle: {color: '#d72323'},
        //         itemStyle: {color: '#d72323'},
        //         symbol: 'none',
        //         sampling: 'lttb',
        //     },
        //     {
        //         data: data4,
        //         name: 'Selver',
        //         type: 'line',
        //         lineStyle: {color: '#e8ce07'},
        //         itemStyle: {color: '#e8ce07'},
        //         symbol: 'none',
        //         sampling: 'lttb',
        //     },
        // ],
    };

    return <ECharts option={options} style={{width: '100%'}} />
}

export default ProductDetails;
