import React, { Component } from 'react'

class Highlight extends Component {
    constructor(props) {
        super(props)

        this.state = {
            content: '',
            links: [],
            showTooltip: false
        }
    }

    componentDidMount() {
        // const { content, links } = this.props.mark.toJSON().data.keyword
        // console.log(this.props.keyword)

        const query = this.props.children.props.children
        this.props.fetchLinks(query)

        // if( this.props.keyword ) {
        //     const { content, links } = this.props.keyword

        //     this.setState({
        //         content: content,
        //         links: links
        //     })
        // }
    }

    onMouseEnter = (e) => {
        e.preventDefault()

        // this.setState({ showTooltip: true })
    }

    onMouseLeave = (e) => {
        e.preventDefault()

        // this.setState({ showTooltip: false })
    }

    onClick = (e) => {
        e.preventDefault()

        // console.log(e.target.textContent)
        const query = this.props.children.props.children
        console.log('query', query)
        this.props.fetchLinks(query)

        // this.props.setResults(this.state.links)
    }
 
    render() {
        const { children, attributes, color } = this.props

        const style = {
            'backgroundColor': color,
            'color': 'black',
            'padding': '.3em',
            'cursor': 'pointer'
        }

        return (
            <span onClick={this.onClick} onMouseEnter={this.onMouseEnter} onMouseLeave={this.onMouseLeave} style={style} {...{ attributes }}>{children}</span>
        )
    }
}

export default Highlight