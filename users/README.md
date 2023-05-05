# Componente user

## User Model
O próprio django já oferece um modelo de usuário padrão, ao mesmo tempo ele oferece um modelo de usuário que deve ser usado para a construção de modelos de usuário personalizados: o <code>AbstractBaseUser</code>. Qualquer aplicação real tende a utilizá-lo em detrimento do padrão já oferecido pelo django por causa de sua flexibilidade. O modelo de usuário que implementei possui os seguintes atributos:

- username (charfield)
- email (charfield)
- password (charfield)
- is_active (boolean, default = True)
- is_staff (boolean, default = False)
- date_joined (datetimefield, default = timezone.now)

Para que o modelo funcione adequadamente é preciso implemntar um manager. Porém como este modelo implementa os mesmos atributos do modelo padrão do django é possível reaproveitar o manager padrão também: o <code>UserManager</code>. Caso o projeto em que este componente seja usado exigir outros atributos, um manager diferente terá de ser implementado.

## User Serializer
O serializador serializa e desserializa todos os atributos do modelo, ele implementa três métodos: <code>validate, create e update</code>.

### Validate
Apenas ao escrever o serializador herdando do serializador do DRF e implementando os atributos também do DRF, o método is_valid() fica disponível e já validará os atributos. So alterei o comportamento do atributo password passando o <code>validate_password</code> do django. Ainda assim impletei o método validate que é executado após a validação dos atributos por parte do DRF, ele verifica se o email passado já não é de um usuário existente. Essa validação toda ocorre em dois cenários: o de criação de um novo usuário e o de atualização dos dados de um usuário existente.

### Create
O <code>create</code> é método que é invocado quando o <code>serializer.save()</code> é invocado. Ele apenas chama o método <code>create_user()</code> de <code>MyUser</code>.

### Update
Esse método atualiza os atributos da instância de <code>MyUser</code>, tomando o cuidado de criptografar a senha no processo e depois salva o usuário.

## User Views

## Tests

