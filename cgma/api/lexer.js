const { run: lexerRun } = require('../../cgmalexer');

module.exports = async (req, res) => {
    const { source_code } = req.body;
    const [tokens, errors] = lexerRun('<stdin>', source_code);

    res.status(200).json({
        tokens: tokens.map(token => ({ type: token.type, value: token.value })),
        errors: errors.map(error => error.as_string())
    });
};