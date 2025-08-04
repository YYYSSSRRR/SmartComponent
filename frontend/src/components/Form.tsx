// FormComponent.tsx
import React, { forwardRef, useImperativeHandle } from 'react'
import { Form, Input, Button } from 'antd'

const FormComponent = forwardRef((props, ref) => {
  const [form] = Form.useForm()

  useImperativeHandle(ref, () => ({
    setFieldValue: (field: string, value: any) => {
      form.setFieldsValue({ [field]: value })
    },
    submitForm: () => {
      form.submit()
    }
  }))

  const onFinish = (values: any) => {
    console.log('表单提交成功：', values)
  }

  return (
    <Form form={form} onFinish={onFinish} layout="vertical">
      <Form.Item label="用户名" name="username" rules={[{ required: true }]}>
        <Input placeholder="请输入用户名" />
      </Form.Item>
      <Button type="primary" htmlType="submit">提交</Button>
    </Form>
  )
})

export default FormComponent