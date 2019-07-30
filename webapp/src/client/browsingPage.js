import React, { Fragment } from 'react';
import {css, StyleSheet} from 'aphrodite';
import ListingCard from './listingCard';

export default class browsingPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            listings:[]
        }
    };

    componentDidMount() {
        //call api to get available listings
    }

    render() {
        return(
            <ListingCard
                // img={}
                // title={}
                // condition={}
                // price={}
                // location={}
                // owner={}
                // listedDate={}
            />
        )
    }
}