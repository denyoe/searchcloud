import React, { Component } from 'react';
import './TextEditor.css';
import { Editor } from 'slate-react';
import { Value, Data } from 'slate';
import Highlight from '../Highlight';
import { TXT, TXT2 } from './sample.js';
import axios from 'axios';

const initialValue = Value.fromJSON({
    document: {
        nodes: [
            {
                object: 'block',
                type: 'paragraph',
                nodes: [
                    {
                        object: 'text',
                        leaves: [
                            {
                                text: TXT2
                            }
                        ]
                    }
                ]
            }
        ]
    }
})

const styles = {
    'width': '50%'
}

const URL = 'http://127.0.0.1:8000/api/search_fetch'

// const initialResults = () => {
//     return (
//         <div className="c-inital">
//             <h4>Google</h4>
//             <ul>
//                 <li><a href="">link</a></li>
//                 <li><a href="">link</a></li>
//                 <li><a href="">link</a></li>
//             </ul>
//         </div>
//     )
// }

const mapLinks = (links, key) => {
    return (
        <div key={key}>
            <h4>{key}</h4>
            <ul>
                {
                    links.map(item => {
                        return <li key={item.rank}><a target="_" href={item.link}>{item.title}</a></li>
                    })
                }
            </ul>
        </div>
    )
}

// const printOrigin = (str) => {
//     return <h4>{str}</h4>
// }

const mapOrigins = (origins) => {
    const origins_array = Object.keys(origins)

    return (
        <div>
            {
                origins_array.map(item => {
                    return mapLinks(origins[item], item)
                })
            }
        </div>
    )
}

const Results = (props) => {
    const { links, isEmpty, isLoading } = props

    if ( isLoading ) {
        return (
            <div className="c-inital">
                Loading...
            </div>
        )
    }

    if( !isEmpty && links.length ) {
        const transformedLinks = []

        links.map(item => {
            if (item.origin in transformedLinks) {
                transformedLinks[item.origin].push({
                    link: item.link,
                    rank: item.rank,
                    title: item.title,
                    desc: item.desc
                })
            } else {
                transformedLinks[item.origin] = [{
                    link: item.link,
                    rank: item.rank,
                    title: item.title,
                    desc: item.desc
                }]
            }
        })

        return (
            <div className="c-item">
                {
                    mapOrigins(transformedLinks)
                }
            </div>
        )
    }
    
    if ( !links.length && !isEmpty ) {
        return (
            <div className="c-inital">
                Select a Section and Press <em>Ctrl+H</em> to analysis
            </div>
        )
    }

    return (
        <div className="c-inital">
            Empty Set
            </div>
    )
    
}

// const initialResults = `
//     <div className="c-inital">
//         <h4>Google</h4>
//         <ul>
//             <li><a href="">link</a></li>
//             <li><a href="">link</a></li>
//             <li><a href="">link</a></li>
//         </ul>
//     </div>
// `

// const results = {
//     keywords: [
//         {
//             content: 'summer\'s lease hath',
//             links: [
//                 {
//                     "title": "Apple (Latin America)",
//                     "link": "https://www.apple.com/lae/",
//                     "desc": "Discover the innovative world of Apple and shop everything iPhone, iPad, ...",
//                     "origin": "GOOGLE",
//                     "rank": 1
//                 }
//             ]
//         },
//         {
//             content: 'this gives life to thee.',
//             links: [
//                 {
//                     "title": "Apple (Latin America)",
//                     "link": "https://www.shmoop.com/sonnet-18/section-2-lines-9-14-summary.html",
//                     "desc": "Discover the innovative world of Apple and shop everything iPhone, iPad, ...",
//                     "origin": "GOOGLE",
//                     "rank": 1
//                 },
//                 {
//                     "title": "Brainly",
//                     "link": "https://brainly.com/question/3697676",
//                     "desc": "Discover the innovative world of Apple and shop everything iPhone, iPad, ...",
//                     "origin": "GOOGLE",
//                     "rank": 2
//                 }
//             ]
//         }
//     ]
// }

export default class TextEditor extends Component {

    schema = {
        marks: {
            highlight: {
                isAtomic: true,
            },
        },
    }

    decorations = []

    renderMark = (props, editor, next) => {
        const { children, mark, attributes } = props
        switch (mark.type) {
            case 'bold':
                return <strong {...{ attributes }}>{children}</strong>
            case 'italic':
                return <em {...{ attributes }}>{children}</em>
            case 'code':
                return <code {...{ attributes }}>{children}</code>
            case 'underline':
                return <u {...{ attributes }}>{children}</u>
            case 'strikethrough':
                return <strike {...{ attributes }}>{children}</strike>
            case 'highlight':
                return <Highlight {...props} fetchLinks={this.fetchLinks} keyword={this.links} color="yellow" setResults={this.setResults} />
            default:
                return next()
        }
    }

    markPlugin() {
        return {
            renderMark: this.renderMark
        }
    }

    plugins = [
        this.markPlugin()
    ]

    /**
     * Store a reference to the `editor`.
     *
     * @param {Editor} editor
     */

    ref = editor => {
        this.editor = editor
    }
    
    constructor(props) {
        super(props)

        this.state = {
            value: initialValue,
            isLoading: false,
            isEmpty: false,
            links: []
        }
    }

    componentDidMount() {
        // this.mapKeywords(results.keywords)
    }

    mapKeywords = (keywords) => {
        keywords.map(keyword => {
            this.highlight(keyword)
        })
    }

    highlight(keyword, color = 'yellow') {
        const { editor } = this
        const { content } = keyword
        // this.fetchLinks(content)
        const { value } = editor
        const texts = value.document.getTexts()
        // const decorations = []

        // console.log('keyword', keyword)

        texts.forEach(node => {
            const { key, text } = node
            const parts = text.split(content)
            let offset = 0

            parts.forEach((part, i) => {
                if (i !== 0) {
                    this.decorations.push({
                        anchor: { key, offset: offset - content.length },
                        focus: { key, offset },
                        mark: { type: 'highlight', data: Data.fromJSON({ keyword }) },
                    })
                }

                offset = offset + part.length + content.length
            })
        })

        // console.log(decorations, str)

        editor.withoutSaving(() => {
            editor.setDecorations(this.decorations)
        })
    }

    toggleLoading = () => {
        console.log('toggle loading...')
        this.setState({
            isLoading: !this.state.isLoading
        })
    }

    fetchLinks = (keyword) => {
        // axios.post(URL, {
        //     'keywords': [keyword]
        // }).then(data => {
        //     this.setState({
        //         links: data.links
        //     })
        //     console.log(data)
        // })

        let formData = new FormData()
        formData.set('keywords', JSON.stringify(keyword))

        console.log('fetching...')
        this.toggleLoading()

        axios({
            method: 'POST',
            url: URL,
            data: formData,
            config: { headers: { 'Content-Type': 'multipart/form-data' } }
        })
        .then(({ data }) => {
            //handle success
            console.log(data.links)
            this.toggleLoading()
            if(! data.links.length ) {
                this.setState({
                    'isEmpty': true
                })
            } else {
                this.setState({
                    'isEmpty': false
                })
            }
            this.setState({
                links: data.links
            })
        })
        .catch((err) => {
            //handle error
            console.log(err.message)
        })
    }

    setResults = (links) => {
        this.setState({links})
    }

    onChange = ({ value }) => {
        this.setState({ value })
    }

    onKeyDown = (e, editor, next) => {
        // cancel actions not starting with Ctrl key press
        if(! e.ctrlKey )    return next()
        e.preventDefault()

        switch (e.key) {
            case 'b': {
                editor.toggleMark('bold')
                return true
            }
            case 'h': {
                editor.toggleMark('highlight')
                return true
            }
            default:
                return next()
        }
    }

    render() {
        // let RESULTS
        // if( this.state.results !== '' ) {
        //     RESULTS = <initialResults />
        // } else {
        //     RESULTS = 'dd'
        // }

        return(
            <div className="c-main">
                <div className="c-text">
                    <Editor
                        plugins={this.plugins}
                        ref={this.ref}
                        defaultValue={this.state.value}
                        schema={this.schema}
                        onChange={this.onChange}
                        onKeyDown={this.onKeyDown}
                        styles={styles}
                    />
                </div>
                <div className="c-results">
                    {/* <i class="fas fa-igloo"></i> */}
                    <Results isLoading={this.state.isLoading} isEmpty={this.state.isEmpty} links={this.state.links} />
                </div>
            </div>
        )
    }
} 