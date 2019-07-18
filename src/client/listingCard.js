import React, { Component } from "react";
import {css, StyleSheet} from 'aphrodite';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';

const styles = StyleSheet.create({
    card: {
        maxWidth: 700,
        '@media (min-width: 400px)': {
            maxWidth: 300
        }
    }
});

export default class listingCard extends Component {
    render() {
        return(
            <>
                <Card>
                    <CardActionArea>
                        <CardContent>
                            hello
                        </CardContent>
                    </CardActionArea>
                    <CardActions>
                        
                    </CardActions>
                </Card>
            </>
        )
    }
}